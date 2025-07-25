# db.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timezone

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "prompt_store"
COLLECTION_NAME = "prompts"

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_prompt(prompt, embedding, crew_id, agents_data):
    agents_list = [agent.dict() if hasattr(agent, 'dict') else agent for agent in agents_data]
    doc = {
        "crew_id": crew_id,
        "prompt": prompt,
        "embedding": embedding,
        "agents":agents_list,  # ✅ Store YAML content directly
        "created_at" : datetime.now(timezone.utc)
    }
    collection.insert_one(doc)

def find_similar_prompt(embedding: list, threshold: float = 0.9) -> dict | None:
    result = collection.aggregate([
        {
            "$vectorSearch": {
                "index": "embedding_index",
                "path": "embedding",
                "queryVector": embedding,
                "numCandidates": 10,
                "limit": 1,
            }
        },
        {
            "$project": {
                "crew_id": 1,
                "prompt": 1,
                "agents_yaml_path": 1,
                "similarity": { "$meta": "vectorSearchScore" }
            }
        }
    ])

    for doc in result:
        if doc.get("similarity", 0) >= threshold:
            return {
                "crew_id": doc["crew_id"],
                "prompt": doc["prompt"],
                "agents": doc["agents"],
                "similarity": doc.get("similarity", 1.0)
        }


    return None


