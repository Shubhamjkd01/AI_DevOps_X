#!/usr/bin/env bash
echo "========================================================"
echo "  AIDEVOPS - Linux / macOS Startup Launcher"
echo "========================================================"
echo ""

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "[*] Created .env from .env.example."
        echo "[*] Please edit .env with your GEMINI_API_KEY and GITHUB_TOKEN!"
    fi
fi

python3 run_local.py
