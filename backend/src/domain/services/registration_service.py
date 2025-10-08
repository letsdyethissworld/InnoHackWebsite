import logging
from typing import List

from pydantic import BaseModel

from src.domain.models import TeamRegistration
from src.domain.services.telegram_service import TelegramService


class RegistrationRequest(BaseModel):
    """Request model for team registration"""
    teamName: str
    selectedCase: str
    captainName: str
    captainEmail: str
    teamMembers: List[str]
    event: str
    status: str = "pending"


class RegistrationResponse(BaseModel):
    """Response model for registration operations"""
    status: str
    message: str
    registration_id: int | None = None


class RegistrationService:
    """Service for handling team registration business logic"""

    def __init__(self, telegram_service: TelegramService | None = None):
        self.telegram_service = telegram_service
        self._logger = logging.getLogger(__name__)

    def create_registration_from_request(self, request: RegistrationRequest) -> TeamRegistration:
        """Create a domain model from registration request"""
        return TeamRegistration(
            team_name=request.teamName,
            selected_case=request.selectedCase,
            captain_name=request.captainName,
            captain_email=request.captainEmail,
            team_members=",".join(request.teamMembers) if request.teamMembers else "",
            event=request.event,
            status=request.status,
        )

    async def process_registration(self, request: RegistrationRequest) -> RegistrationResponse:
        """Process a new team registration"""
        try:
            # Create domain model
            registration = self.create_registration_from_request(request)

            # Here we would typically save to database
            # For now, we'll simulate getting an ID
            registration_id = await self._save_registration_to_db(registration)

            # Send Telegram notification if service is available
            if self.telegram_service and self.telegram_service.is_initialized():
                await self.telegram_service.send_registration_notification(registration)

            return RegistrationResponse(
                status="success",
                message="Registration saved and admins notified.",
                registration_id=registration_id
            )

        except Exception as e:
            self._logger.error(f"Error processing registration: {e}")
            raise

    async def _save_registration_to_db(self, registration: TeamRegistration) -> int:
        """Save registration to database - this would be implemented with actual DB logic"""
        # TODO: Implement actual database saving logic
        # For now, return a simulated ID
        import random
        return random.randint(1000, 9999)

    def get_registration_by_id(self, registration_id: int) -> TeamRegistration | None:
        """Get registration by ID - this would be implemented with actual DB logic"""
        # TODO: Implement actual database retrieval logic
        # For now, return None
        return None

    def get_all_registrations(self) -> List[TeamRegistration]:
        """Get all registrations - this would be implemented with actual DB logic"""
        # TODO: Implement actual database retrieval logic
        # For now, return empty list
        return []
