import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.api.routers.helpers import get_uow
from src.bootstrap import Bootstrap
from src.domain.models.team_registration import TeamRegistration
from src.domain.services.registration_service import RegistrationRequest
from src.infrastructure.uow import UoW

# Create router
router = APIRouter(prefix="", tags=["registrations"])

logger = logging.getLogger(__name__)


def get_telegram_service():
    """Dependency to get the Telegram service instance"""
    return Bootstrap.bootstrapped().telegram_service


class RegistrationResponse(BaseModel):
    """Response model for registration endpoints"""
    status: str
    message: str
    registration_id: int | None = None


@router.post("/", response_model=RegistrationResponse)
async def create_registration(
    registration_data: RegistrationRequest,
    uow: UoW = Depends(get_uow),
    telegram_service = Depends(get_telegram_service)
) -> RegistrationResponse:
    """Create a new team registration"""
    try:
        # Create domain model from request
        registration = TeamRegistration(
            team_name=registration_data.teamName,
            selected_case=registration_data.selectedCase,
            captain_name=registration_data.captainName,
            captain_email=registration_data.captainEmail,
            team_members=",".join(registration_data.teamMembers),
            event=registration_data.event,
            status=registration_data.status,
        )

        # Save to database
        registration_id = await uow.team_registrations.add(registration)

        # Send Telegram notification if service is available
        if telegram_service and telegram_service.is_initialized():
            # Create a new instance for notification (with ID for logging)
            notification_registration = TeamRegistration(
                id=registration_id,
                team_name=registration_data.teamName,
                selected_case=registration_data.selectedCase,
                captain_name=registration_data.captainName,
                captain_email=registration_data.captainEmail,
                team_members=",".join(registration_data.teamMembers),
                event=registration_data.event,
                status=registration_data.status,
            )
            await telegram_service.send_registration_notification(notification_registration)

        logger.info(f"Registration created successfully: {registration_id}")
        return RegistrationResponse(
            status="success",
            message="Registration saved successfully.",
            registration_id=registration_id
        )

    except Exception as e:
        logger.error(f"Error creating registration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[dict])
async def get_all_registrations(
    uow: UoW = Depends(get_uow)
) -> List[dict]:
    """Get all registrations"""
    try:
        registrations = await uow.team_registrations.get_all()
        return [reg.to_dict() for reg in registrations]

    except Exception as e:
        logger.error(f"Error retrieving registrations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoint - must come before parameterized routes
@router.get("/health")
async def registration_health_check(
    telegram_service = Depends(get_telegram_service)
) -> dict:
    """Health check for registration service"""
    return {
        "status": "healthy",
        "telegram_initialized": telegram_service.is_initialized(),
        "service": "registration"
    }


@router.get("/{registration_id}", response_model=dict)
async def get_registration(
    registration_id: int,
    uow: UoW = Depends(get_uow)
) -> dict:
    """Get a specific registration by ID"""
    try:
        registration = await uow.team_registrations.get_by_id(registration_id)

        if not registration:
            raise HTTPException(status_code=404, detail="Registration not found")

        return registration.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving registration {registration_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{registration_id}", response_model=dict)
async def update_registration(
    registration_id: int,
    registration_data: RegistrationRequest,
    uow: UoW = Depends(get_uow)
) -> dict:
    """Update a registration"""
    try:
        # Get existing registration
        existing_registration = await uow.team_registrations.get_by_id(registration_id)

        if not existing_registration:
            raise HTTPException(status_code=404, detail="Registration not found")

        # Create updated registration
        updated_registration = TeamRegistration(
            id=registration_id,
            team_name=registration_data.teamName,
            selected_case=registration_data.selectedCase,
            captain_name=registration_data.captainName,
            captain_email=registration_data.captainEmail,
            team_members=",".join(registration_data.teamMembers),
            event=registration_data.event,
            status=registration_data.status,
        )

        # Update in database
        await uow.team_registrations.update(updated_registration)

        logger.info(f"Registration updated: {registration_id}")
        return updated_registration.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating registration {registration_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

