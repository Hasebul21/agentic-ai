from sqlalchemy.orm import Session
from db.models import Conversation


def save_conversation(db: Session, user_message: str, ai_response: str, model: str = "gpt-4o-mini") -> Conversation:
    record = Conversation(user_message=user_message, ai_response=ai_response, model=model)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_all_conversations(db: Session) -> list[Conversation]:
    return db.query(Conversation).order_by(Conversation.created_at.desc()).all()


def get_conversation_by_id(db: Session, conversation_id: int) -> Conversation | None:
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()


def delete_conversation(db: Session, conversation_id: int) -> bool:
    record = get_conversation_by_id(db, conversation_id)
    if not record:
        return False
    db.delete(record)
    db.commit()
    return True
