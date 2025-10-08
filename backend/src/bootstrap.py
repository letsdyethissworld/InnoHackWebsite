import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from time import sleep
from typing import Any, AsyncGenerator, Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_core import ValidationError
from starlette.middleware.trustedhost import TrustedHostMiddleware

from src import logger
from src.api.exception_handler import (not_found_handler,
                                       validation_error_handler)
from src.domain.abstract_uow import AbstractUnitOfWork
from src.domain.services.telegram_service import TelegramService, TelegramConfig
from src.exceptions import NotFoundError
from src.infrastructure.adapters.sql_model_adapter import SQLModelAdapter
from src.infrastructure.uow import UoW
from src.settings.settings import settings


@dataclass
class Bootstrapped:
    fast_api: FastAPI
    uow_partial: Callable[..., AbstractUnitOfWork]
    sql_model_adapter: SQLModelAdapter
    telegram_service: TelegramService


class Bootstrap:
    _bootstrapped: Bootstrapped | None = None

    def __call__(self, *args: Any, **kwds: Any) -> Bootstrapped:
        if Bootstrap._bootstrapped is not None:
            return Bootstrap._bootstrapped

        logger.setup_logger(settings.run_settings.logging_level)

        logging.info("BOOTSTRAPPING SERVICE - %s", settings.api.application_name)

        logging.info("BOOTSTRAPPING - Postgres")
        sql_model_adapter = SQLModelAdapter(
            database_host=settings.database.host,
            database_port=settings.database.port,
            database_user=settings.database.user,
            database_password=settings.database.password,
            database_name=settings.database.name,
            application_name=settings.api.application_name,
        )

        logging.info("BOOTSTRAPPING - Telegram Service")
        telegram_config = TelegramConfig(
            bot_token=settings.telegram.bot_token,
            admin_user_ids=settings.telegram.admin_user_ids,
        )
        telegram_service = TelegramService(config=telegram_config)

        fast_api = Bootstrap.bootstrap_fastapi(
            sql_model_adapter=sql_model_adapter,
            telegram_service=telegram_service,
        )

        logging.info("BOOTSTRAPPING - UoW")

        def uow_partial() -> UoW:
            return UoW(sql_model_adapter=sql_model_adapter)

        Bootstrap._bootstrapped = Bootstrapped(
            fast_api=fast_api,
            uow_partial=uow_partial,
            sql_model_adapter=sql_model_adapter,
            telegram_service=telegram_service,
        )

        logging.info("BOOTSTRAPPING Completed")
        return Bootstrap._bootstrapped

    @staticmethod
    def bootstrapped() -> Bootstrapped:
        """Use this method to access the bootstrapped instance."""
        if Bootstrap._bootstrapped is None:
            raise RuntimeError("Bootstrapped singleton not initialized")
        return Bootstrap._bootstrapped

    @staticmethod
    def bootstrap_fastapi(
        sql_model_adapter: SQLModelAdapter,
        telegram_service: TelegramService,
    ) -> FastAPI:
        logging.debug("BOOTSTRAPPING - fast api")
        # Use root_path for production (with nginx) but allow it to be disabled for local development
        root_path = "" if settings.run_settings.env == "dev" else "/api"
        fast_api = FastAPI(
            title=f"{settings.api.application_name} API",
            description=settings.api.description,
            root_path=root_path,
            root_path_in_servers=False,  # This ensures OpenAPI docs work both locally and in production
            docs_url="/docs",
            redoc_url="/redoc",
            openapi_url="/openapi.json",
        )
        Bootstrap.add_exception_handlers(fast_api)

        logging.debug("BOOTSTRAPPING - fast api cors")
        fast_api.add_middleware(
            CORSMiddleware,
            allow_origin_regex=r"^https?://(localhost(:\d+)?|example\.com|staging\.example\.com)(:\d+)?$",
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["*"],
        )

        fast_api.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.api.trusted_hosts,
        )

        @asynccontextmanager
        async def lifespan_context(app: FastAPI) -> AsyncGenerator[None, None]:
            """Handle application startup and shutdown events."""
            # Startup logic
            connected = False
            while not connected:
                try:
                    await sql_model_adapter.create_engine()
                    connected = True
                except Exception as e:
                    logging.error(
                        f"Unable to connect to DB - Retrying... Error: {str(e)}"
                    )
                    sleep(3)

            # Initialize Telegram service if enabled
            if settings.telegram.enabled:
                try:
                    await telegram_service.initialize()
                    logging.info("Telegram service initialized successfully")
                except Exception as e:
                    logging.error(f"Failed to initialize Telegram service: {e}")
                    # Continue without Telegram service

            yield

            # Shutdown logic
            logging.info(
                "Application shutting down. Waiting for background tasks to complete..."
            )

            # Shutdown Telegram service
            if settings.telegram.enabled:
                try:
                    await telegram_service.shutdown()
                    logging.info("Telegram service shut down successfully")
                except Exception as e:
                    logging.error(f"Error shutting down Telegram service: {e}")

            # Close database connections
            await sql_model_adapter.dispose_engine()

        # Assign the lifespan context manager to the FastAPI app
        fast_api.router.lifespan_context = lifespan_context

        # Include routers
        from src.api.routers.registrations.router import router as registration_router
        from src.api.routers.telegram.router import router as telegram_settings_router

        fast_api.include_router(registration_router, prefix="/api/registrations")
        fast_api.include_router(telegram_settings_router, prefix="/api/settings/telegram")

        return fast_api

    @staticmethod
    def add_exception_handlers(fast_api: FastAPI) -> None:
        # Cast exception handlers to the appropriate type to satisfy type checking
        fast_api.add_exception_handler(NotFoundError, not_found_handler)  # type: ignore
        fast_api.add_exception_handler(
            ValidationError, validation_error_handler  # type: ignore
        )
