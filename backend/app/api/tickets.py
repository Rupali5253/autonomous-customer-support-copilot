from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ticket import TicketCreate
from app.core.security import get_current_user


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post("/")
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_ticket = Ticket(
        customer_id=current_user["user_id"],
        subject=ticket_data.subject,
        description=ticket_data.description,
        priority=ticket_data.priority
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "message": "Ticket created successfully",
        "ticket_id": new_ticket.id,
        "status": new_ticket.status
    }

@router.get("/")
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tickets = (
        db.query(Ticket)
        .filter(Ticket.customer_id == current_user["user_id"])
        .order_by(Ticket.created_at.desc())
        .all()
    )

    return {
        "tickets": tickets
    }

@router.get("/assigned")
def get_assigned_tickets(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "agent":
        raise HTTPException(
            status_code=403,
            detail="Only agents can access assigned tickets"
        )

    tickets = (
        db.query(Ticket)
        .filter(
            Ticket.assigned_to == current_user["user_id"]
        )
        .order_by(Ticket.created_at.desc())
        .all()
    )

    return {
        "tickets": tickets
    }

@router.get("/all")
def get_all_tickets(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can access all tickets"
        )

    tickets = (
        db.query(Ticket)
        .order_by(Ticket.created_at.desc())
        .all()
    )

    return {
        "tickets": tickets
    }

@router.get("/{ticket_id}")
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    ticket = (
        db.query(Ticket)
        .filter(
            Ticket.id == ticket_id,
            Ticket.customer_id == current_user["user_id"]
        )
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket

@router.put("/{ticket_id}/assign")
def assign_ticket(
    ticket_id: int,
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can assign tickets"
        )

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    agent = (
        db.query(User)
        .filter(
            User.id == agent_id,
            User.role == "agent"
        )
        .first()
    )

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Support agent not found"
        )

    ticket.assigned_to = agent.id
    ticket.status = "assigned"

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket assigned successfully",
        "ticket_id": ticket.id,
        "assigned_to": agent.id,
        "assigned_agent": agent.name,
        "status": ticket.status
    }

@router.put("/{ticket_id}/status")
def update_ticket_status(
    ticket_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    ticket = (
        db.query(Ticket)
        .filter(
            Ticket.id == ticket_id
        )
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Role permission check
    if current_user["role"] not in ["agent", "manager"]:
        raise HTTPException(
            status_code=403,
            detail="Only agents or managers can update ticket status"
        )

    # Agent can update only their assigned tickets
    if (
        current_user["role"] == "agent"
        and ticket.assigned_to != current_user["user_id"]
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only update tickets assigned to you"
        )

    allowed_statuses = [
        "open",
        "assigned",
        "in_progress",
        "resolved",
        "closed"
    ]

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid ticket status"
        )

    ticket.status = new_status

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket status updated successfully",
        "ticket_id": ticket.id,
        "status": ticket.status
    }