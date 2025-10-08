import logging
import os
from pathlib import Path
from typing import Any

from dynaconf import Dynaconf
from pydantic import BaseModel, model_validator


class DatabaseSettings(BaseModel):
    """
    Configuration for the PostgreSQL database.
    """

    host: str
    port: int
    user: str
    password: str
    # To which DB we are connecting.
    name: str

    @model_validator(mode="before")
    @classmethod
    def normalize_field_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        """
        Convert field names to lowercase.
        As Dynaconf doesn't convert filed name and pydantic expect lowercase field names,
        we need to do it manually for case with env variables.

        Args:
            values: Dictionary of field names and values

        Returns:
            Dictionary with lowercase field names
        """
        return {k.lower(): v for k, v in values.items()}

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "host": "localhost",
                    "port": 5432,
                    "user": "postgres",
                    "password": "secret",
                    "name": "mydb",
                }
            ]
        }
    }


class APISettings(BaseModel):
    # The name of the application. It used in logging and other places.
    application_name: str
    # The description of the application. It used FastAPI.
    description: str
    # The secret key for the JWT session token.
    session_jwt_secret: str
    # The expiration time of the JWT session token in seconds.
    session_token_expiration_time: int
    # The list of trusted hosts. It used in FastAPI to prevent host header attacks.
    trusted_hosts: list[str]


class RunSettings(BaseModel):
    # The level of logging (e.g. DEBUG, INFO, WARNING, ERROR, CRITICAL  )
    logging_level: str
    # The environment name
    env: str | None = None
    # The directory with static files for frontend. Also we are saving data to this directory.
    static_files_dir: str
    # Url of the frontend application. Required for redirect urls.
    application_url: str
    # It's used to generate the redirect URL for the google oauth callback when we are running locally.
    backend_url: str | None = None

    # API prefix for the application. Empty for dev, /api for other environments
    @property
    def api_prefix(self) -> str:
        """Get the API prefix for the application."""
        if self.env == "dev":
            return ""
        return "/api"

    @property
    def base_url(self) -> str:
        """Get the base URL for the application."""
        if self.env == "dev":
            if not self.backend_url:
                raise ValueError("backend_url is required for dev environment")
            return self.backend_url
        return self.application_url

    def __init__(self, **data):
        super().__init__(**data)


class ServerSettings(BaseModel):
    """Web server configuration settings.

    This class contains all the settings related to the server configuration,
    including host, port, and various performance and security settings.
    """

    # The host address to bind the server to. Use '0.0.0.0' to make the server accessible from other machines.
    host: str = "0.0.0.0"
    # The port number to bind the server to.
    port: int = 8080
    # Controls the lifespan events of the application. 'on' enables lifespan events, 'off' disables them.
    lifespan: str = "on"
    # Whether to trust X-Forwarded-* headers. Important for running behind a reverse proxy.
    proxy_headers: bool = True
    # Comma-separated list of IP addresses to trust for X-Forwarded-* headers. '*' means trust all.
    forwarded_allow_ips: str = "*"
    # The number of seconds to keep a connection alive when no data is being sent.
    timeout_keep_alive: int = 5
    # Enable auto-reload of the application when code changes are detected. Useful for development.
    reload: bool = False
    # The number of worker processes to run. Set to 1 for development, increase for production.
    workers: int = 1


class TelegramSettings(BaseModel):
    """Telegram bot configuration settings."""

    # Telegram bot token for sending notifications
    bot_token: str = ""
    # List of Telegram user IDs to send notifications to
    admin_user_ids: list[int] = []
    # Whether Telegram notifications are enabled
    enabled: bool = True

    @model_validator(mode="before")
    @classmethod
    def normalize_field_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        """
        Convert field names to lowercase.
        As Dynaconf doesn't convert filed name and pydantic expect lowercase field names,
        we need to do it manually for case with env variables.
        """
        return {k.lower(): v for k, v in values.items()}


class Settings(BaseModel):
    database: DatabaseSettings
    api: APISettings
    run_settings: RunSettings
    server: ServerSettings
    telegram: TelegramSettings


class SettingsFactory:
    """
    Factory class for creating Settings instances from Dynaconf settings.
    """

    @classmethod
    def create_from_dynaconf(cls, dynaconf_settings: Dynaconf) -> Settings:
        """
        Create a Settings instance from Dynaconf settings.

        Args:
            dynaconf_settings: The Dynaconf settings object

        Returns:
            Settings instance populated with values from Dynaconf
        """
        data: dict[str, Any] = {}

        for field_name, field_info in Settings.model_fields.items():
            # Get the field type
            field_type = field_info.annotation

            # Handle other nested models - check if it's a subclass of BaseModel
            if isinstance(field_type, type) and issubclass(field_type, BaseModel):
                data[field_name] = cls._process_nested_model(
                    dynaconf_settings, field_name, field_type
                )
            else:
                # This is a simple field
                data[field_name] = cls._process_simple_field(
                    dynaconf_settings, field_name
                )

        return Settings(**data)

    @classmethod
    def _process_nested_model(
        cls, dynaconf_settings: Dynaconf, field_name: str, field_type: type[BaseModel]
    ) -> BaseModel:
        """
        Process a nested Pydantic model field.

        Args:
            dynaconf_settings: The Dynaconf settings object
            field_name: The name of the field
            field_type: The type of the field (a Pydantic model class)

        Returns:
            An instance of the field type populated with values from Dynaconf
        """
        nested_data = {}

        # Extract nested fields from Dynaconf
        if hasattr(dynaconf_settings, field_name):
            dynaconf_section = getattr(dynaconf_settings, field_name)

            # If dynaconf already has a structured section
            if isinstance(dynaconf_section, dict):
                nested_data = dynaconf_section
            else:
                # Try to get each field of the nested model from dynaconf
                for nested_field in field_type.model_fields:
                    key = f"{field_name}.{nested_field}"
                    if (
                        # Dynaconf's get method is dynamically typed
                        hasattr(dynaconf_settings, key)
                        or dynaconf_settings.get(key) is not None  # type: ignore
                    ):
                        nested_data[nested_field] = dynaconf_settings.get(key)  # type: ignore

        # Create an instance of the nested model
        return field_type(**nested_data)

    @classmethod
    def _process_simple_field(cls, dynaconf_settings: Dynaconf, field_name: str) -> Any:
        """
        Process a simple (non-nested) field.

        Args:
            dynaconf_settings: The Dynaconf settings object
            field_name: The name of the field

        Returns:
            The value of the field from Dynaconf or None if not found
        """
        if hasattr(dynaconf_settings, field_name):
            return getattr(dynaconf_settings, field_name)
        return None


current_dir = Path(__file__).parent.absolute()

DEFAULT_ENV = "dev"

# Initialize Dynaconf settings for the web part of the application
_settings = Dynaconf(
    settings_files=[  # Paths to config files
        str(current_dir / "settings.toml"),
        str(current_dir / "settings.dev.toml"),
        str(current_dir / "settings.staging.toml"),
    ],
    environments=True,  # Enable environments
    load_dotenv=False,  # Don't load .env files
    envvar_prefix="DYNACONF",  # Prefix for environment variables
    env_switcher="ENV",  # Environment variable to switch environments
    env=DEFAULT_ENV,  # This is the env which will be used if ENV is not set
    # For test we set ENV to test in conftest.py
)

# Create an instance of the Settings model with values from Dynaconf
settings = SettingsFactory.create_from_dynaconf(_settings)
settings.run_settings.env = os.environ.get("ENV", DEFAULT_ENV)

# Export settings as module attributes
__all__ = ["settings"]
