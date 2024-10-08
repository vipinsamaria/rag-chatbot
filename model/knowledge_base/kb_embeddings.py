import json
import pickle
from sentence_transformers import SentenceTransformer

def prepare_kb_embeddings():
    try:
        # Load the pre-trained model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        knowledgebase = []
        knowledgebase_embeddings = {}

        # Read the JSONL file and encode the knowledge base
        with open("apollo_knowledgebase.jsonl", 'r') as f:
            for line in f:
                entry = json.loads(line.strip())
                text = entry['text']
                source = entry['source']

                # Append the entry to the knowledge base
                knowledgebase.append({"text": text, "source": source})

                # Compute the embedding for the current text
                embedding = model.encode(text, convert_to_tensor=True)
                
                # Store the embedding with its text for later retrieval
                knowledgebase_embeddings[text] = embedding

        # Save precomputed embeddings and knowledgebase to files
        with open('knowledgebase_embeddings.pkl', 'wb') as f:
            pickle.dump(knowledgebase_embeddings, f)

        with open('knowledgebase.pkl', 'wb') as f:
            pickle.dump(knowledgebase, f)

        print("Knowledge base embeddings precomputed and saved successfully.")
    
    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

prepare_kb_embeddings()