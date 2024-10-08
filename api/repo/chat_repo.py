from db.models import Chat
from sqlalchemy.exc import SQLAlchemyError


def get_previous_messages(user_id, db):
    try:
        chat_obj = Chat()
        chat_history = chat_obj.get_last_n_messages(user_id=user_id, db=db)
        reponse = []
        for chat in chat_history:
            reponse.insert(0,{
                "user": chat.query,
                "bot": chat.answer
            })
        return reponse
    except SQLAlchemyError as e:
        # Handle SQLAlchemy-related errors
        print(f"SQLAlchemy Error: {str(e)}")
        error_message = "A database error occurred. Please try again later."
        return error_message

    except Exception as e:
        # Handle other exceptions
        print(f"Error: {str(e)}")
        error_message = "An unexpected error occurred. Please try again later."
        return error_message