from abc import ABC, abstractmethod
from typing import Self

from src.domain.repositories.abstract_team_registration_repository import (
    AbstractTeamRegistrationRepository,
)
from src.infrastructure.adapters.sql_model_adapter import SQLModelAdapter


class AbstractUnitOfWork(ABC):
    sql_model_adapter: SQLModelAdapter
    team_registrations: AbstractTeamRegistrationRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type=None, exc_val=None, exc_tb=None) -> None:
        # exc_type, exc_val, exc_tb are required by Python's async context manager protocol.
        # Without them, Python cannot properly implement the 'async with' statement
        # as it wouldn't know how to handle exceptions that occur within the context.
        # The method signature must match exactly what Python expects.
        raise NotImplementedError
