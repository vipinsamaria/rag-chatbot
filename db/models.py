from datetime import datetime
import uuid
from db.configure import Base, engine
from sqlalchemy import Column, String, DateTime, desc

# Chat model
class Chat(Base):
    __tablename__ = "chats"
    id = Column(String, primary_key=True, index=True)
    user_id= Column(String)
    query = Column(String)
    answer = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow) 

    @classmethod
    def create(cls, user_id: str, query: str, answer: str, db):
        new_chat = cls(id= str(uuid.uuid4()), user_id=user_id, query=query, answer=answer, created_at=datetime.utcnow())
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        return new_chat

    @classmethod
    def get_last_n_messages(cls, user_id: str, db, limit: int=None):
        if limit :
            return (db.query(cls)
                    .filter(cls.user_id == user_id)
                    .order_by(desc(cls.created_at)) 
                    .limit(limit)  # Retrieve the last n messages
                    .all())
        else:
            return (db.query(cls)
                    .filter(cls.user_id == user_id)
                    .order_by(desc(cls.created_at)) 
                    .all())


# Create the database tables
Base.metadata.create_all(bind=engine)