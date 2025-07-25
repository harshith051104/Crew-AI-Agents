# crew_runner.py

import yaml
import os
from crewai import Agent, Task, Crew, Process, LLM

gemini_api_key = os.getenv("GEMINI_API_KEY")

print(f"Using Gemini API Key: {gemini_api_key}")

gemini_llm = LLM(model="gemini/gemini-2.5-pro",api_key=os.getenv("GEMINI_API_KEY"))


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def run_crew(crew_dir: str, user_prompt: str) -> str:
    try:
        # Load agents.yaml and tasks.yaml
        agents_file = os.path.join(crew_dir, "agents.yaml")
        tasks_file = os.path.join(crew_dir, "tasks.yaml")

        agents_data = load_yaml(agents_file)
        tasks_data = load_yaml(tasks_file)

        agents = []
        agent_map = {}

        # Build Agent objects without tools
        for key, data in agents_data.items():
            # print(key, data)
            # continue
            agent = Agent(
                role=data["role"],
                goal=data["goal"],
                backstory=data["backstory"],
                verbose=True,
                memory=True,
                tools=[],
                llm=gemini_llm  # ⛔ no tools
            )
            agents.append(agent)
            agent_map[key] = agent

        # Build Task objects (assign first agent to all tasks)
        tasks = []
        for key, task_info in tasks_data.items():
            # print(key, task_info)
            # continue
            task = Task(
                description=task_info["description"],
                expected_output=task_info["expected_output"],
                agent=agents[0],  # Assign to first agent
                tools=[]  # ⛔ no tools
            )
            tasks.append(task)

        # Assemble and run Crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential
        )

        result = crew.kickoff(inputs={"prompt": user_prompt})
        return result
    except Exception as e:
        print("❌ Error running crew:", str(e))
        return f"Error: {str(e)}"
