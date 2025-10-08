import logging

from fastapi import Request
from fastapi.staticfiles import StaticFiles

from src.bootstrap import Bootstrap
from src.settings.settings import settings

bootstrapped = Bootstrap()()

app = bootstrapped.fast_api

app.mount(
    "/static",
    StaticFiles(directory=settings.run_settings.static_files_dir),
    name="static",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    return response
