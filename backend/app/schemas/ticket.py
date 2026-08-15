from enum import Enum

from pydantic import BaseModel


class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TicketCreate(BaseModel):
    subject: str
    description: str
    priority: TicketPriority = TicketPriority.medium