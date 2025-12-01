#!/bin/bash

echo "Starting AI Agent Gateway..."
echo

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo
    echo "IMPORTANT: Please edit .env and add your GCP credentials!"
    echo
    read -p "Press enter to continue..."
fi

# Check if virtual environment exists
if [ ! -d venv ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo
echo "Starting server on http://localhost:8080"
echo "Press Ctrl+C to stop"
echo
uvicorn services.gateway.app:app --host 127.0.0.1 --port 8080 --reload
