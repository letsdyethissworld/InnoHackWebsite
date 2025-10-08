import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.api.routers.helpers import get_uow
from src.bootstrap import Bootstrap
from src.settings.settings import settings

# Create router
router = APIRouter(prefix="", tags=["telegram-settings"])

logger = logging.getLogger(__name__)


def get_telegram_service():
    """Dependency to get the Telegram service instance"""
    return Bootstrap.bootstrapped().telegram_service


class TelegramSettingsResponse(BaseModel):
    """Response model for Telegram settings"""
    bot_token_configured: bool
    admin_user_ids: List[int]
    initialized: bool


class UpdateTelegramSettingsRequest(BaseModel):
    """Request model for updating Telegram settings"""
    admin_user_ids: List[int]


@router.get("/", response_model=TelegramSettingsResponse)
async def get_telegram_settings(
    telegram_service = Depends(get_telegram_service)
) -> TelegramSettingsResponse:
    """Get current Telegram notification settings"""
    try:
        return TelegramSettingsResponse(
            bot_token_configured=bool(settings.telegram.bot_token),
            admin_user_ids=settings.telegram.admin_user_ids,
            initialized=telegram_service.is_initialized()
        )

    except Exception as e:
        logger.error(f"Error retrieving Telegram settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/test")
async def send_test_notification(
    telegram_service = Depends(get_telegram_service)
) -> dict:
    """Send a test notification to all subscribed users"""
    try:
        if not telegram_service.is_initialized():
            raise HTTPException(
                status_code=503,
                detail="Telegram service is not initialized"
            )

        await telegram_service.send_test_message()
        logger.info("Test notification sent successfully")

        return {
            "status": "success",
            "message": "Test notification sent to all subscribed users"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending test notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))
