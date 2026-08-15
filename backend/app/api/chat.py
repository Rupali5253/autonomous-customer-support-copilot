from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ticket import Ticket
from app.schemas.chat import ChatRequest
from app.services.intent_service import detect_intent
from app.core.security import get_current_user
from app.services.llm_service import generate_llm_response
from app.rag.rag_service import generate_rag_response
from app.services.escalation_service import check_escalation
from app.models.user import User

def get_next_agent(db: Session):
    agents = (
        db.query(User)
        .filter(User.role == "agent")
        .order_by(User.id.asc())
        .all()
    )

    if not agents:
        return None

    # Find agent with the fewest active tickets
    agent_loads = []

    for agent in agents:

        active_tickets = (
            db.query(Ticket)
            .filter(
                Ticket.assigned_to == agent.id,
                Ticket.status.in_([
                    "assigned",
                    "in_progress"
                ])
            )
            .count()
        )

        agent_loads.append(
            (agent, active_tickets)
        )

    # Select agent with lowest workload
    agent_loads.sort(
        key=lambda x: x[1]
    )

    return agent_loads[0][0]

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(
    chat_data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    # 1. Detect user intent
   
    intent_result = detect_intent(
        chat_data.message
    )


    # 2. Check whether human escalation is required
    escalation_result = check_escalation(
        chat_data.message,
        intent_result["intent"],
        intent_result["priority"]
    )
    
    # 3. Generate response
    #
    # General conversation → normal LLM response
    # Support issue → RAG + Llama response

    if not intent_result["ticket_required"]:

        ai_response = generate_llm_response(
            chat_data.message
        )

        return {
            "message": ai_response,
            "intent": intent_result["intent"],
            "ticket_created": False,
            "escalation_required": escalation_result["escalation_required"],
            "escalation_reason": escalation_result["escalation_reason"]
        }
        

    # Support issue → use RAG
    ai_response = generate_rag_response(
        chat_data.message,
        top_k=3
    )

    assigned_agent = get_next_agent(db)
    
    # 4. Create support ticket
    new_ticket = Ticket(
        customer_id=current_user["user_id"],
        subject=intent_result["intent"],
        description=chat_data.message,
        status="assigned" if assigned_agent else "open",
        priority=intent_result["priority"],
        intent=intent_result["intent"],
        ai_response=ai_response,
        assigned_to=assigned_agent.id if assigned_agent else None,
        escalation_reason=escalation_result["escalation_reason"]
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    # 5. Return AI response + ticket information
    return {
        "message": ai_response,
        "intent": intent_result["intent"],
        "priority": intent_result["priority"],
        "ticket_created": True,
        "ticket_id": new_ticket.id,
        "status": new_ticket.status,
        "assigned_to": new_ticket.assigned_to,
        "escalation_required": escalation_result["escalation_required"],
        "escalation_reason": escalation_result["escalation_reason"]
    }