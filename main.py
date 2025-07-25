from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import shutil

from embedding import get_prompt_embedding
from db import find_similar_prompt, save_prompt, collection
from gemini_client import generate_agents_yaml
from crew_generator import generate_crew_yaml_files
from crew_runner import run_crew
from dotenv import load_dotenv

load_dotenv(override=True)

app = FastAPI()

class PromptInput(BaseModel):
    prompt: str

BASE_DIR = "data/crews"

@app.post("/generate_agents")
def generate_agents_for_prompt(data: PromptInput):
    prompt = data.prompt.strip()
    print(f"📥 User Prompt: {prompt}")
    
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    try:
        # Step 1: Get prompt embedding
        embedding = get_prompt_embedding(prompt)
        match = find_similar_prompt(embedding)

        # Step 2: Reuse if match found (above similarity threshold)
        if match:
            print(f"🔁 Similar prompt detected! Reusing crew {match['crew_id']} (score: {match['similarity']:.4f})")
            crew_dir = os.path.dirname(match["agents_yaml_path"])
            output = run_crew(crew_dir, prompt)
            return {
                "crew_id": match["crew_id"],
                "status": "existing",
                "similarity": match["similarity"],
                "output": output
            }

        # Step 3: Ask Gemini to generate agents
        agents = generate_agents_yaml(prompt)
        if not agents:
            raise ValueError("Gemini did not return any agents.")

        print("✅ Generated agents:")
        for i, (key, agent) in enumerate(agents.items(), start=1):
            print(f"Agent {i}: {agent['role']}")

        # Step 4: Save agents.yaml and tasks.yaml
        crew_id, crew_dir = generate_crew_yaml_files(agents, prompt)
        
        print(f"✅ Crew YAML files created at {crew_dir}")
        
        agents_yaml_path = os.path.join(crew_dir, "agents.yaml")
        if not os.path.exists(agents_yaml_path):
            raise FileNotFoundError(f"YAML not created at {agents_yaml_path}")

        # Step 5: Save to MongoDB
        agents_list = list(agents.values())
        save_prompt(prompt, embedding, crew_id, agents_list)
        # Step 6: Run CrewAI agents
        output = run_crew(crew_dir, prompt)

        return {
            "crew_id": crew_id,
            "status": "new",
            "output": output
        }

    except Exception as e:
        print("❌ Server error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{crew_id}")
def get_agents(crew_id: str):
    agents_path = os.path.join(BASE_DIR, crew_id, "agents.yaml")
    if not os.path.exists(agents_path):
        raise HTTPException(status_code=404, detail="Crew not found")

    with open(agents_path, "r") as f:
        return {"crew_id": crew_id, "agents": f.read()}

@app.delete("/agents/{crew_id}")
def delete_crew(crew_id: str):
    crew_path = os.path.join(BASE_DIR, crew_id)
    if not os.path.exists(crew_path):
        raise HTTPException(status_code=404, detail="Crew not found")

    shutil.rmtree(crew_path)
    result = collection.delete_one({"crew_id": crew_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Crew not found in database")

    return {"message": f"Crew {crew_id} deleted successfully"}
