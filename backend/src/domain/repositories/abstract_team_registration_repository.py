from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.models import TeamRegistration


class AbstractTeamRegistrationRepository(ABC):
    """Abstract repository for team registration operations"""

    @abstractmethod
    async def add(self, registration: TeamRegistration) -> int:
        """Add a new team registration and return its ID"""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, registration_id: int) -> Optional[TeamRegistration]:
        """Get a team registration by ID"""
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[TeamRegistration]:
        """Get all team registrations"""
        raise NotImplementedError

    @abstractmethod
    async def update(self, registration: TeamRegistration) -> None:
        """Update an existing team registration"""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, registration_id: int) -> None:
        """Delete a team registration by ID"""
        raise NotImplementedError
