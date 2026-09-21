from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.models.message import Message


def create_message(db: Session, message: Message) -> Message:
    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_messages(
    db: Session,
    search: str | None = None,
    category: str | None = None,
    priority: str | None = None
) -> list[Message]:

    query = db.query(Message)

    if search:
        search_term = f"%{search}%"

        query = query.filter(
            or_(
                Message.sender.ilike(search_term),
                Message.subject.ilike(search_term),
                Message.body.ilike(search_term)
            )
        )

    if category:
        query = query.filter(Message.category == category)

    if priority:
        query = query.filter(Message.priority == priority)

    return query.all()


def get_message_by_id(
    db: Session,
    message_id: int
) -> Message | None:

    return db.query(Message).filter(
        Message.id == message_id
    ).first()


def delete_message(
    db: Session,
    message: Message
) -> None:

    db.delete(message)
    db.commit()


def update_message_analysis(
    db: Session,
    message: Message,
    category: str,
    priority: str,
    sentiment: str,
    summary: str,
    suggested_action: str
) -> Message:

    message.category = category
    message.priority = priority
    message.sentiment = sentiment
    message.summary = summary
    message.suggested_action = suggested_action

    db.commit()
    db.refresh(message)

    return message


def get_summary(db: Session) -> dict:

    total = db.query(func.count(Message.id)).scalar()

    category_rows = (
        db.query(
            Message.category,
            func.count(Message.id)
        )
        .group_by(Message.category)
        .all()
    )

    priority_rows = (
        db.query(
            Message.priority,
            func.count(Message.id)
        )
        .group_by(Message.priority)
        .all()
    )

    return {
        "total_messages": total,
        "by_category": {
            category: count
            for category, count in category_rows
            if category is not None
        },
        "by_priority": {
            priority: count
            for priority, count in priority_rows
            if priority is not None
        }
    }