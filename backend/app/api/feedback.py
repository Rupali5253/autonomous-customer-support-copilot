from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.feedback import Feedback
from app.models.feedback_review import FeedbackReview
from app.models.ticket import Ticket
from app.core.security import get_current_user
from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackReviewUpdate
)

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)


@router.post("/")
def create_feedback(
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # ==========================================
    # CHECK WHETHER TICKET EXISTS
    # ==========================================

    ticket = (
        db.query(Ticket)
        .filter(
            Ticket.id == feedback_data.ticket_id,
            Ticket.customer_id == current_user["user_id"]
        )
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # ==========================================
    # CHECK EXISTING FEEDBACK
    # ==========================================

    existing_feedback = (
        db.query(Feedback)
        .filter(
            Feedback.customer_id == current_user["user_id"],
            Feedback.ticket_id == feedback_data.ticket_id
        )
        .first()
    )

    # ==========================================
    # UPDATE EXISTING FEEDBACK
    # ==========================================

    if existing_feedback:

        old_rating = existing_feedback.rating

        existing_feedback.rating = feedback_data.rating
        existing_feedback.comment = feedback_data.comment

        # --------------------------------------
        # If changed to NOT HELPFUL
        # --------------------------------------

        if feedback_data.rating == "not_helpful":

            existing_review = (
                db.query(FeedbackReview)
                .filter(
                    FeedbackReview.feedback_id == existing_feedback.id,
                    FeedbackReview.review_status == "pending"
                )
                .first()
            )

            if not existing_review:

                review = FeedbackReview(
                    feedback_id=existing_feedback.id,
                    ticket_id=feedback_data.ticket_id,
                    review_status="pending"
                )

                db.add(review)

        # --------------------------------------
        # If changed to HELPFUL
        # --------------------------------------

        elif feedback_data.rating == "helpful":

            pending_reviews = (
                db.query(FeedbackReview)
                .filter(
                    FeedbackReview.feedback_id == existing_feedback.id,
                    FeedbackReview.review_status == "pending"
                )
                .all()
            )

            for review in pending_reviews:
                db.delete(review)

        db.commit()
        db.refresh(existing_feedback)

        return {
            "message": "Feedback updated successfully",
            "feedback_id": existing_feedback.id,
            "ticket_id": existing_feedback.ticket_id,
            "rating": existing_feedback.rating
        }

    # ==========================================
    # CREATE NEW FEEDBACK
    # ==========================================

    new_feedback = Feedback(
        customer_id=current_user["user_id"],
        ticket_id=feedback_data.ticket_id,
        rating=feedback_data.rating,
        comment=feedback_data.comment
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    # ==========================================
    # CREATE REVIEW FOR NEGATIVE FEEDBACK
    # ==========================================

    if feedback_data.rating == "not_helpful":

        review = FeedbackReview(
            feedback_id=new_feedback.id,
            ticket_id=feedback_data.ticket_id,
            review_status="pending"
        )

        db.add(review)
        db.commit()
        db.refresh(review)

    return {
        "message": "Feedback submitted successfully",
        "feedback_id": new_feedback.id,
        "ticket_id": new_feedback.ticket_id,
        "rating": new_feedback.rating
    }

@router.get("/my")
def get_my_feedback(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    feedback = (
        db.query(Feedback)
        .filter(
            Feedback.customer_id == current_user["user_id"]
        )
        .order_by(Feedback.created_at.desc())
        .all()
    )

    return {
        "feedback": feedback
    }

@router.get("/assigned")
def get_assigned_feedback(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "agent":
        raise HTTPException(
            status_code=403,
            detail="Only agents can access assigned feedback"
        )

    feedback = (
        db.query(Feedback)
        .join(
            Ticket,
            Feedback.ticket_id == Ticket.id
        )
        .filter(
            Ticket.assigned_to == current_user["user_id"]
        )
        .order_by(Feedback.created_at.desc())
        .all()
    )

    return {
        "feedback": feedback
    }

@router.get("/all")
def get_all_feedback(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can access all feedback"
        )

    feedback = (
        db.query(Feedback)
        .order_by(Feedback.created_at.desc())
        .all()
    )

    return {
        "feedback": feedback
    }

@router.get("/analytics")
def get_feedback_analytics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can access feedback analytics"
        )

    total_feedback = (
        db.query(Feedback)
        .count()
    )

    helpful_feedback = (
        db.query(Feedback)
        .filter(
            Feedback.rating == "helpful"
        )
        .count()
    )

    not_helpful_feedback = (
        db.query(Feedback)
        .filter(
            Feedback.rating == "not_helpful"
        )
        .count()
    )

    if total_feedback > 0:
        satisfaction_rate = (
            helpful_feedback / total_feedback
        ) * 100
    else:
        satisfaction_rate = 0

    return {
        "total_feedback": total_feedback,
        "helpful": helpful_feedback,
        "not_helpful": not_helpful_feedback,
        "satisfaction_rate": round(
            satisfaction_rate, 2
        )
    }

@router.get("/reviews")
def get_feedback_reviews(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can access feedback reviews"
        )

    reviews = (
        db.query(FeedbackReview)
        .filter(
            FeedbackReview.review_status == "pending"
        )
        .order_by(
            FeedbackReview.created_at.desc()
        )
        .all()
    )

    return {
        "reviews": reviews
    }

@router.put("/reviews/{review_id}")
def update_feedback_review(
    review_id: int,
    review_data: FeedbackReviewUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can review feedback"
        )

    review = (
        db.query(FeedbackReview)
        .filter(
            FeedbackReview.id == review_id
        )
        .first()
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Feedback review not found"
        )

    allowed_statuses = [
        "pending",
        "reviewed"
    ]

    if review_data.review_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid review status"
        )

    review.review_status = review_data.review_status
    review.review_comment = review_data.review_comment

    db.commit()
    db.refresh(review)

    return {
        "message": "Feedback review updated successfully",
        "review_id": review.id,
        "review_status": review.review_status,
        "review_comment": review.review_comment
    }

@router.get("/improvements")
def get_feedback_improvements(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can access improvement data"
        )

    reviews = (
        db.query(
            FeedbackReview,
            Feedback,
            Ticket
        )
        .join(
            Feedback,
            FeedbackReview.feedback_id == Feedback.id
        )
        .join(
            Ticket,
            FeedbackReview.ticket_id == Ticket.id
        )
        .filter(
            FeedbackReview.review_status == "reviewed",
            Feedback.rating == "not_helpful"
        )
        .order_by(
            FeedbackReview.created_at.desc()
        )
        .all()
    )

    improvements = []

    for review, feedback, ticket in reviews:
        improvements.append({
            "review_id": review.id,
            "ticket_id": ticket.id,
            "intent": ticket.intent,
            "priority": ticket.priority,
            "customer_question": ticket.description,
            "ai_response": ticket.ai_response,
            "customer_feedback": feedback.comment,
            "review_comment": review.review_comment,
            "review_status": review.review_status
        })

    return {
        "improvements": improvements
    }

@router.get("/improvements/by-intent")
def get_improvements_by_intent(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can access improvement analytics"
        )

    results = (
        db.query(
            Ticket.intent,
            Feedback.rating
        )
        .join(
            Feedback,
            Feedback.ticket_id == Ticket.id
        )
        .filter(
            Feedback.rating == "not_helpful"
        )
        .all()
    )

    intent_counts = {}

    for intent, rating in results:

        if intent not in intent_counts:
            intent_counts[intent] = 0

        intent_counts[intent] += 1

    return {
        "negative_feedback_by_intent": intent_counts
    }

@router.get("/improvements/suggestions")
def get_improvement_suggestions(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can access improvement suggestions"
        )

    results = (
        db.query(Ticket.intent)
        .join(
            Feedback,
            Feedback.ticket_id == Ticket.id
        )
        .filter(
            Feedback.rating == "not_helpful"
        )
        .all()
    )

    intent_counts = {}

    for (intent,) in results:

        if intent not in intent_counts:
            intent_counts[intent] = 0

        intent_counts[intent] += 1

    suggestions = []

    for intent, count in intent_counts.items():

        if count >= 2:
            suggestions.append({
                "intent": intent,
                "negative_feedback_count": count,
                "suggestion": (
                    f"Review and improve the knowledge base "
                    f"and AI responses for {intent} issues."
                )
            })

    return {
        "suggestions": suggestions
    }