import logging
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from src.domain.models import TeamRegistration
from src.domain.repositories.abstract_team_registration_repository import (
    AbstractTeamRegistrationRepository,
)
from src.exceptions import NotFoundError


class TeamRegistrationRepository(AbstractTeamRegistrationRepository):
    """SQLAlchemy-based repository for team registration operations"""

    def __init__(self, session: AsyncSession):
        self._session = session
        self._logger = logging.getLogger(__name__)

    async def add(self, registration: TeamRegistration) -> int:
        """Add a new team registration and return its ID"""
        try:
            self._session.add(registration)
            await self._session.flush()  # Flush to get the ID without committing
            registration_id = registration.id
            self._logger.info(f"Added new team registration: {registration.team_name} (ID: {registration_id})")
            return registration_id
        except IntegrityError as e:
            self._logger.error(f"Failed to add team registration: {e}")
            raise

    async def get_by_id(self, registration_id: int) -> Optional[TeamRegistration]:
        """Get a team registration by ID"""
        try:
            result = await self._session.execute(
                select(TeamRegistration).where(TeamRegistration.id == registration_id)
            )
            registration = result.scalar_one_or_none()
            if registration:
                self._logger.debug(f"Found registration with ID: {registration_id}")
            else:
                self._logger.debug(f"No registration found with ID: {registration_id}")
            return registration
        except Exception as e:
            self._logger.error(f"Error retrieving registration {registration_id}: {e}")
            raise

    async def get_all(self) -> List[TeamRegistration]:
        """Get all team registrations"""
        try:
            result = await self._session.execute(
                select(TeamRegistration).order_by(TeamRegistration.registration_date.desc())
            )
            registrations = result.scalars().all()
            self._logger.debug(f"Retrieved {len(registrations)} registrations")
            return list(registrations)
        except Exception as e:
            self._logger.error(f"Error retrieving all registrations: {e}")
            raise

    async def update(self, registration: TeamRegistration) -> None:
        """Update an existing team registration"""
        try:
            if not registration.id:
                raise ValueError("Registration ID is required for update")

            # Get existing registration
            existing = await self.get_by_id(registration.id)
            if not existing:
                raise NotFoundError(TeamRegistration, f"with id {registration.id}")

            # Update fields
            for field in ["team_name", "selected_case", "captain_name", "captain_email",
                         "team_members", "registration_date", "event", "status", "updated_at"]:
                setattr(existing, field, getattr(registration, field))

            self._logger.info(f"Updated registration: {registration.id}")
        except NotFoundError:
            raise
        except Exception as e:
            self._logger.error(f"Error updating registration {registration.id}: {e}")
            raise

    async def delete(self, registration_id: int) -> None:
        """Delete a team registration by ID"""
        try:
            result = await self._session.execute(
                delete(TeamRegistration).where(TeamRegistration.id == registration_id)
            )

            if result.rowcount == 0:
                raise NotFoundError(TeamRegistration, f"with id {registration_id}")

            self._logger.info(f"Deleted registration: {registration_id}")
        except NotFoundError:
            raise
        except Exception as e:
            self._logger.error(f"Error deleting registration {registration_id}: {e}")
            raise
