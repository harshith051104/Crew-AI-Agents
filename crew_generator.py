# crew_generator.py

import os
import yaml
import uuid

BASE_DIR = "data/crews"

def generate_crew_yaml_files(agents: dict, prompt: str) -> tuple[str, str]:
    # Generate a new crew ID
    crew_id = str(uuid.uuid4())
    crew_dir = os.path.join(BASE_DIR, crew_id)
    os.makedirs(crew_dir, exist_ok=True)

    # Save agents.yaml
    agents_path = os.path.join(crew_dir, "agents.yaml")
    with open(agents_path, "w") as f:
        yaml.dump(agents, f)

    # Create single prompt-based task
    task_data = {
        "prompt_response_task": {
            "description": f"""
            Your task is to produce a high-quality response for the following user prompt:
            \"{prompt}\"

            Collaborate as a team to brainstorm, analyze, and generate the best possible answer.
            """,
            "expected_output": "Your final answer MUST directly address the user's prompt with clarity and creativity."
        }
    }

    tasks_path = os.path.join(crew_dir, "tasks.yaml")
    with open(tasks_path, "w") as f:
        yaml.dump(task_data, f)

    return crew_id, crew_dir
