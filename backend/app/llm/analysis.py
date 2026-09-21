from pydantic import BaseModel

from app.schemas.message import Category, Priority, Sentiment


class MessageAnalysis(BaseModel):
    category: Category
    priority: Priority
    sentiment: Sentiment
    summary: str
    suggested_action: str