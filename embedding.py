# embedding.py

from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_prompt_embedding(prompt: str) -> list[float]:
    embedding = model.encode(prompt, convert_to_numpy=True, normalize_embeddings=True)
    return embedding.tolist()
