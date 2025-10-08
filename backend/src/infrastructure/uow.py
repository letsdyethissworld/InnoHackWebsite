import logging
from typing import Self

from src.domain.abstract_uow import AbstractUnitOfWork
from src.domain.repositories.abstract_team_registration_repository import (
    AbstractTeamRegistrationRepository,
)
from src.infrastructure.adapters.sql_model_adapter import SQLModelAdapter
from src.infrastructure.repositories.team_registration_repository import (
    TeamRegistrationRepository,
)


class UoW(AbstractUnitOfWork):
    sql_model_adapter: SQLModelAdapter
    team_registrations: AbstractTeamRegistrationRepository

    def __init__(self, sql_model_adapter: SQLModelAdapter) -> None:
        self.sql_model_adapter = sql_model_adapter

    async def __aenter__(self) -> Self:
        logging.debug("UoW __aenter__: Creating new session")
        self.__sql_model_session = await self.sql_model_adapter.get_session()
        logging.debug("UoW __aenter__: Session created")

        # Initialize repositories
        self.team_registrations = TeamRegistrationRepository(self.__sql_model_session)

        return self

    async def __aexit__(self, exc_type=None, exc_val=None, exc_tb=None) -> None:
        if self.__sql_model_session:
            try:
                if exc_type is not None:
                    logging.error(
                        f"Rolling back due to error: {exc_type.__name__}: {exc_val}"
                    )
                    await self.__sql_model_session.rollback()
                else:
                    try:
                        await self.__sql_model_session.commit()
                        logging.debug("UoW __aexit__: Session committed successfully")
                    except Exception as e:
                        logging.error(f"Error committing session: {str(e)}")
                        await self.__sql_model_session.rollback()
                        logging.debug(
                            "UoW __aexit__: Session rolled back after commit error"
                        )
                        raise e  # Re-raise the commit error
            except Exception as e:
                # Catch any errors during session handling to prevent background tasks from failing
                # This is particularly important for background event handlers
                if "asyncio.CancelledError" in str(e.__class__):
                    logging.info(
                        "Session cleanup cancelled - this is normal during shutdown"
                    )
                else:
                    logging.error(f"Error during session cleanup: {str(e)}")
                    raise e  # Re-raise the error
            finally:
                try:
                    await self.__sql_model_session.close()
                    logging.debug("UoW __aexit__: Session closed")
                except Exception as e:
                    # Just log any errors during session close, don't re-raise
                    logging.error(f"Error closing session: {str(e)}")
