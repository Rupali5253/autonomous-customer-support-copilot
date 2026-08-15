from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db.base import Base


class FeedbackReview(Base):
    __tablename__ = "feedback_reviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    feedback_id = Column(
        Integer,
        ForeignKey("feedback.id"),
        nullable=False
    )

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id"),
        nullable=False
    )

    review_status = Column(
        String(20),
        default="pending",
        nullable=False
    )

    review_comment = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )