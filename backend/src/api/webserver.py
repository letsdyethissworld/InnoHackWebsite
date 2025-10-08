"""Webserver configuration module."""

import logging

import uvicorn

from src.settings.settings import settings


def get_server_config() -> dict:
    """Get server configuration based on environment."""
    # Get base configuration from settings
    config = {
        "host": settings.server.host,
        "port": settings.server.port,
        "lifespan": settings.server.lifespan,
        "proxy_headers": settings.server.proxy_headers,
        "forwarded_allow_ips": (
            settings.server.forwarded_allow_ips
            + ","
            + ",".join(settings.api.trusted_hosts)
        ),
        "timeout_keep_alive": settings.server.timeout_keep_alive,
        "reload": settings.server.reload,
        "workers": settings.server.workers,
    }

    return config


def run_server() -> None:
    """Run the FastAPI server with environment-specific configuration."""
    config = get_server_config()
    logging.info(
        "Starting server in %s environment with config: %s",
        settings.run_settings.env,
        config,
    )

    uvicorn.run(
        "src.entrypoints.main:app",
        **config,
    )


if __name__ == "__main__":
    run_server()
