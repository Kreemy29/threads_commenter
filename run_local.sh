#!/bin/bash

# Setup Python virtual environment if not already activated
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "Setting up virtual environment..."
    if [ ! -d "venv" ]; then
        python -m venv venv
    fi
    
    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # Install dependencies
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "Please update .env with your DeepSeek API key before continuing."
    exit 1
fi

# Run the FastAPI application
echo "Starting the comment service..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 