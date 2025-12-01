# AI Agent Gateway

This project implements an AI agent gateway service.

## Setup

1.  **Environment Variables**:
    Copy `.env.example` to `.env` and fill in the required values.
    ```bash
    cp .env.example .env
    ```

2.  **Dependencies**:
    Install the required dependencies.
    ```bash
    pip install -r requirements.txt
    ```

## Running Locally

To run the gateway service locally:

```bash
uvicorn services.gateway.app:app --host 0.0.0.0 --port 8080 --reload
```

## Running with Docker

1.  **Build the image**:
    ```bash
    docker build -t agent-gateway -f docker/Dockerfile .
    ```

2.  **Run with Docker Compose**:
    ```bash
    docker-compose up
    ```
