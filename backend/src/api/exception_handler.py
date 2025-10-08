from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError

from src.exceptions import NotFoundError


async def not_found_handler(request: Request, exception: NotFoundError):
    """Handle NotFoundError that when we try to get a record that does not exist"""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exception)},
    )


async def validation_error_handler(request: Request, exception: ValidationError):
    """Handle ValidationError that when Pydantic validation fails"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=exception.json(),
    )
