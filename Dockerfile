FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install git since the agent performs physical repo mutations
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn pydantic requests pygithub streamlit openai python-dotenv

# Copy the rest of the application
COPY . .

# Expose the port for the OpenEnv Agent API
EXPOSE 8080

# Command to natively run the FastAPI backend server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
