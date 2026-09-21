from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Category(str, Enum):
    INCIDENT = "Incident"
    REQUEST = "Request"
    COMPLAINT = "Complaint"
    INQUIRY = "Inquiry"
    GENERAL = "General"


class Priority(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Sentiment(str, Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"


class MessageCreate(BaseModel):
    sender: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    body: str = Field(min_length=1)


class MessageResponse(BaseModel):
    id: int
    sender: str
    subject: str
    body: str

    category: Category | None = None
    priority: Priority | None = None
    sentiment: Sentiment | None = None
    summary: str | None = None
    suggested_action: str | None = None

    created_at: datetime