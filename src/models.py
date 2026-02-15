"""Database models for activities and participants"""

from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many relationship
activity_participants = Table(
    'activity_participants',
    Base.metadata,
    Column('activity_id', Integer, ForeignKey('activity.id'), primary_key=True),
    Column('participant_email', String, ForeignKey('participant.email'), primary_key=True)
)


class Activity(Base):
    """Activity model"""
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    schedule = Column(String)
    max_participants = Column(Integer)

    # Relationship with participants
    participants = relationship(
        "Participant",
        secondary=activity_participants,
        back_populates="activities"
    )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "schedule": self.schedule,
            "max_participants": self.max_participants,
            "participants": [p.email for p in self.participants]
        }


class Participant(Base):
    """Participant/Student model"""
    __tablename__ = "participant"

    email = Column(String, primary_key=True, index=True)
    activities = relationship(
        "Activity",
        secondary=activity_participants,
        back_populates="participants"
    )
