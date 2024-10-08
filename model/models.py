import os
from sentence_transformers import util
import openai

from db.models import Chat
from sqlalchemy.exc import SQLAlchemyError

from model.utils.utils import get_knowledge_base, preprocess_query, process_response


# Initialize OpenAI API Key
key = os.getenv('OPENAI_API_KEY')
openai.api_key = key


# Get Knowledge Base Data
knowledgebase_embeddings, knowledgebase, model = get_knowledge_base()

def generate_gpt_response(query: str, context: str) -> str:
    response = openai.ChatCompletion.create(
    model="gpt-4o-mini", 
    messages=[
            {"role": "system", "content": os.getenv('GENERAL_CHAT_PROMPT','')},
            {"role": "user", "content": "User Query: " + query + " , " "System Generated Response: " + context}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def process_query(db, query: str) -> str:
    try:
        query = preprocess_query(query)
        
        chat_obj = Chat()
        last_5_messages = chat_obj.get_last_n_messages(user_id=os.getenv('USER_ID'), limit=5, db=db)
        modified_query = query
        if last_5_messages is not None:
            for message in last_5_messages:
                modified_query = message.query + ", " + modified_query
        query_embedding = model.encode(modified_query, convert_to_tensor=True)

        best_match = None
        highest_similarity = -1
        threshold = 0.5  # Adjust this threshold as needed

        for response, response_embedding in knowledgebase_embeddings.items():
            similarity = util.pytorch_cos_sim(query_embedding, response_embedding).item()

            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = response

        if highest_similarity > threshold:
            processed_response = process_response(best_match)
            gpt_response = generate_gpt_response(query, processed_response)
            
            # Save the chat record
            chat_obj.create(user_id=os.getenv("USER_ID"), query=query, answer=gpt_response, db=db)
            return gpt_response

        error_message = "I'm not sure how to answer that. Could you rephrase?"
        chat_obj.create(user_id=os.getenv("USER_ID"), query=query, answer=error_message, db=db)
        return error_message

    except SQLAlchemyError as e:
        # Handle SQLAlchemy-related errors
        print(f"SQLAlchemy Error: {str(e)}")
        error_message = "A database error occurred. Please try again later."
        # Optionally, log the error details for debugging
        return error_message

    except Exception as e:
        # Handle other exceptions
        print(f"Error: {str(e)}")
        error_message = "An unexpected error occurred. Please try again later."
        return error_message