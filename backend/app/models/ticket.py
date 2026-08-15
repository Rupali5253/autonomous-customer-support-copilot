from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    subject = Column(String(200), nullable=False)

    description = Column(Text, nullable=False)

    status = Column(
        String(30),
        default="open",
        nullable=False
    )

    priority = Column(
        String(20),
        default="medium",
        nullable=False
    )

    intent = Column(
        String(100),
        nullable=True
    )

    ai_response = Column(
        Text,
        nullable=True
    )

    assigned_to = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    escalation_reason = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )