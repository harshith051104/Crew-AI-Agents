# gemini_client.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
import yaml

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 2048,
}

system_prompt = """
You're an expert in creating AI agent teams.
For the given user prompt, determine how many agents are needed and generate a list of agents.
Each agent must have:
- role
- goal
- backstory

Return the result as a valid YAML dictionary under a top-level key called "agents".
"""

model = genai.GenerativeModel(model_name="gemini-2.0-flash", generation_config=generation_config)

def generate_agents_yaml(prompt: str) -> dict:
    chat = model.start_chat()
    response = chat.send_message(f"{system_prompt}\n\nUser Prompt:\n{prompt}")
    
    try:
        content = response.text.strip()
        print("🧠 Gemini raw output:\n", content)

        if content.startswith("```"):
            content = content.strip("`")
            content = content.replace("yaml\n", "", 1).strip()

        parsed_yaml = yaml.safe_load(content)

        agents_list = parsed_yaml["agents"]

        # ✅ Convert list to dict: agent1, agent2, etc.
        if isinstance(agents_list, list):
            return {
                f"agent{i+1}": agent for i, agent in enumerate(agents_list)
            }

        return agents_list  # already a dict

    except Exception as e:
        raise ValueError(f"Failed to parse Gemini response as YAML: {e}\n\nRaw response:\n{content}")
