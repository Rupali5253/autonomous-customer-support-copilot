from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    ticket_id: int
    rating: str
    comment: str | None = None


class FeedbackReviewUpdate(BaseModel):
    review_status: str
    review_comment: str | None = None