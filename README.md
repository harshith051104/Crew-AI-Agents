# Crew AI Agents

This project allows you to create and manage teams of AI agents that work together to accomplish tasks. It uses Gemini to generate the agent configurations and CrewAI to run the agent crews.

## Description

This application takes a user's prompt and dynamically creates a team of AI agents to fulfill the request. If a similar prompt has been processed before, it reuses the existing agent configuration to save time and resources. Otherwise, it generates a new team of agents using the Gemini API, saves the configuration, and then runs the crew to get the results. All prompt and agent data is stored in a MongoDB database for future use.

## Features

* **Dynamic Agent Generation**: Automatically creates AI agent teams based on user prompts.
* **Prompt Similarity Matching**: Finds and reuses existing agent crews for similar prompts to improve efficiency.
* **MongoDB Integration**: Stores and retrieves prompt embeddings and agent configurations.
* **CrewAI Execution**: Runs the generated agent crews to perform tasks.
* **FastAPI Endpoints**: Provides a simple API to generate agents, retrieve agent configurations, and delete crews.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/harshith051104/crew-ai-agents.git](https://github.com/harshith051104/crew-ai-agents.git)
    cd crew-ai-agents
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**

    Create a `.env` file in the root directory of the project and add the following, replacing the placeholder values with your actual credentials. You can get a Gemini API key from Google AI Studio and a MongoDB URI from MongoDB Atlas.

    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    MONGODB_URI="YOUR_MONGODB_URI"
    OPENAI_API_KEY="dummy"
    ```

## Usage

You can interact with the application through the provided FastAPI endpoints.

First, run the application using uvicorn:

```bash
uvicorn main:app --reload
```

Then, you can send requests to the following endpoints:

### Generate Agents

* **Endpoint**: `POST /generate_agents`
* **Description**: Creates a new crew of agents or reuses an existing one based on the prompt.
* **Body**:

    ```json
    {
      "prompt": "Your task prompt here"
    }
    ```

### Get Agents

* **Endpoint**: `GET /agents/{crew_id}`
* **Description**: Retrieves the `agents.yaml` configuration for a specific crew.

### Delete Crew

* **Endpoint**: `DELETE /agents/{crew_id}`
* **Description**: Deletes a crew's configuration files and its corresponding entry from the database.

### Sample Output

When you send a new prompt to the `/generate_agents` endpoint, you will see output in your console similar to this:

📥 User Prompt: "Create a marketing campaign for a new line of sustainable sneakers."

✅ Generated agents:

Agent 1: Marketing Strategist

Agent 2: Content Creator

Agent 3: Social Media Manager

✅ Crew YAML files created at data/crews/a1b2c3d4-e5f6-a7b8-c9d0-e1f2a3b4c5d6

✅ Crew a1b2c3d4-e5f6-a7b8-c9d0-e1f2a3b4c5d6 and its agents saved to the database.

The API will return a JSON response with the crew ID, status, and the final output from the crew's execution.

```json
{
  "crew_id": "a1b2c3d4-e5f6-a7b8-c9d0-e1f2a3b4c5d6",
  "status": "new",
  "output": "Here is the comprehensive marketing campaign for the new sustainable sneakers..."
}

