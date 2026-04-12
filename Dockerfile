FROM python:3.11-slim

WORKDIR /app

# CRITICAL: Ensure all Python imports resolve from /app
# Without this, grader modules (tasks.task_1.grader) fail to import
# in subprocesses spawned by the validator
ENV PYTHONPATH=/app

# Install git since the agent performs physical repo mutations
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install uv for rapid OpenEnv submission dependency resolution
RUN pip install --no-cache-dir uv

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies using hyper-fast uv pip
RUN uv pip install --system --no-cache -r requirements.txt
RUN uv pip install --system fastapi uvicorn pydantic requests pygithub streamlit openai python-dotenv openenv pyyaml

# Copy the rest of the application
COPY . .

# Verify graders are importable at build time (fail-fast)
RUN python -c "from tasks.task_1.grader import grade; print('task_1 grader OK:', grade(action_type='analyze'))"
RUN python -c "from tasks.task_2.grader import grade; print('task_2 grader OK:', grade(action_type='analyze'))"
RUN python -c "from tasks.task_3.grader import grade; print('task_3 grader OK:', grade(action_type='analyze'))"

# Expose the port for the OpenEnv Agent API (Hugging Face Default)
EXPOSE 7860

# Command to natively run the FastAPI backend server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
