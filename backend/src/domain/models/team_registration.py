from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlmodel import Field, SQLModel


class TeamRegistration(SQLModel, table=True):
    """SQLModel for team registration database table"""
    __tablename__ = "team_registrations"

    id: Optional[int] = Field(default=None, primary_key=True)
    team_name: str = Field(sa_column=Column(String(255), nullable=False))
    selected_case: str = Field(sa_column=Column(String(255), nullable=False))
    captain_name: str = Field(sa_column=Column(String(255), nullable=False))
    captain_email: str = Field(sa_column=Column(String(255), nullable=False))
    team_members: str = Field(sa_column=Column(Text, nullable=False))  # JSON string of team members
    registration_date: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        sa_column=Column(String(255), nullable=False)
    )
    event: str = Field(sa_column=Column(String(255), nullable=False))
    status: str = Field(default="pending", sa_column=Column(String(50), nullable=False))
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(TIMESTAMP, nullable=False)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(TIMESTAMP, nullable=False)
    )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "teamName": self.team_name,
            "selectedCase": self.selected_case,
            "captainName": self.captain_name,
            "captainEmail": self.captain_email,
            "teamMembers": [member.strip() for member in self.team_members.split(",") if member.strip()] if self.team_members else [],
            "registrationDate": self.registration_date,
            "event": self.event,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TeamRegistration":
        """Create from dictionary"""
        team_members = data.get("teamMembers", [])
        if isinstance(team_members, list):
            team_members_str = ",".join(team_members)
        else:
            team_members_str = str(team_members) if team_members else ""

        # Handle registration_date - use current time if not provided
        registration_date = data.get("registrationDate")
        if not registration_date:
            registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return cls(
            id=data.get("id"),
            team_name=data.get("teamName", ""),
            selected_case=data.get("selectedCase", ""),
            captain_name=data.get("captainName", ""),
            captain_email=data.get("captainEmail", ""),
            team_members=team_members_str,
            registration_date=registration_date,
            event=data.get("event", ""),
            status=data.get("status", "pending"),
        )
