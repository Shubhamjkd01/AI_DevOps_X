FROM python:3.11-slim

WORKDIR /app

# Install git since the agent performs physical repo mutations
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install uv for rapid OpenEnv submission dependency resolution
RUN pip install --no-cache-dir uv

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies using hyper-fast uv pip
RUN uv pip install --system --no-cache -r requirements.txt
RUN uv pip install --system fastapi uvicorn pydantic requests pygithub streamlit openai python-dotenv openenv

# Copy the rest of the application
COPY . .

# Expose the port for the OpenEnv Agent API
EXPOSE 8000

# Command to natively run the FastAPI backend server mapping to the new 3-Component Pattern
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]
