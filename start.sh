#!/bin/bash
echo "Installing dependencies via uv..."
uv sync

echo "Starting FastAPI Server..."
uv run uvicorn main:app --host 0.0.0.0 --port 8080 --reload &

echo "Starting ngrok tunnel..."
ngrok http 8080
