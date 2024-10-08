import os
import pickle
import re
from sentence_transformers import SentenceTransformer


def preprocess_query(query: str) -> str:
    # Replace all special characters with an empty string
    query = re.sub(r'[^A-Za-z0-9\s]', '', query)
    return query.lower().strip()

def process_response(response: str) -> str:
    """
    Dynamically summarizes a given response by removing unnecessary details.
    """
    # Remove any text between square brackets (usually references or image links)
    response = re.sub(r'\[.*?\]', '', response)
    
    # Remove excessive newlines, tabs, etc.
    response = re.sub(r'\s+', ' ', response)

    # Split response into sentences
    sentences = re.split(r'(?<=\.)\s+', response)

    # Select the first few key sentences as a summary
    summary = " ".join(sentences[:])  # You can adjust the number of sentences returned

    return summary


def get_knowledge_base():
    # Check if the embeddings file exists before loading
    if os.path.exists('model/knowledge_base/knowledgebase_embeddings.pkl'):
        # Load precomputed knowledgebase embeddings
        with open('model/knowledge_base/knowledgebase_embeddings.pkl', 'rb') as f:
            knowledgebase_embeddings = pickle.load(f)

        # Load the knowledgebase topics
        with open('model/knowledge_base/knowledgebase.pkl', 'rb') as f:
            knowledgebase = pickle.load(f)

        # Load the same model used for encoding the knowledge base
        model = SentenceTransformer('all-MiniLM-L6-v2')
        return knowledgebase_embeddings, knowledgebase, model
    else:
        raise FileNotFoundError("Precomputed knowledgebase embeddings not found. Please run 'prepare_kb_embeddings()' first.")
