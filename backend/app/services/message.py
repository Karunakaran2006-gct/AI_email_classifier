from sqlalchemy.orm import Session

from app.models.message import Message
from app.repositories.message import (
    create_message,
    get_messages,
    get_message_by_id,
    delete_message,
    update_message_analysis,
    get_summary
)
from app.schemas.message import MessageCreate
from app.llm.gemini import GeminiService


def create_message_service(
    db: Session,
    message_data: MessageCreate
) -> Message:

    message = Message(
        sender=message_data.sender,
        subject=message_data.subject,
        body=message_data.body
    )

    return create_message(db, message)


def get_messages_service(
    db: Session,
    search: str | None = None,
    category: str | None = None,
    priority: str | None = None
) -> list[Message]:

    return get_messages(
        db,
        search=search,
        category=category,
        priority=priority
    )

def get_summary_service(db: Session) -> dict:
    return get_summary(db)


def get_message_by_id_service(
    db: Session,
    message_id: int
) -> Message | None:

    return get_message_by_id(db, message_id)


def analyze_message_service(
    db: Session,
    message_id: int
) -> Message | None:

    # 1. Get the message from the database
    message = get_message_by_id(db, message_id)

    if message is None:
        return None

    # 2. Create the LLM service
    llm = GeminiService()

    # 3. Send the message to Gemini for analysis
    analysis = llm.analyze(
        subject=message.subject,
        body=message.body
    )

    # 4. Save the AI analysis into the database
    return update_message_analysis(
        db=db,
        message=message,
        category=analysis.category.value,
        priority=analysis.priority.value,
        sentiment=analysis.sentiment.value,
        summary=analysis.summary,
        suggested_action=analysis.suggested_action
    )

def delete_message_service(
    db: Session,
    message_id: int
) -> bool:

    message = get_message_by_id(db, message_id)

    if message is None:
        return False

    delete_message(db, message)

    return True