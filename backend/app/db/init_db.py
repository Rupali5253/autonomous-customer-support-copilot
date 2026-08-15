from app.db.base import Base
from app.db.database import engine

# Import all models

from app.models import User
from app.models.ticket import Ticket
from app.models.feedback import Feedback
from app.models.feedback_review import FeedbackReview

# Create all tables
Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully.")