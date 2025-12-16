# Clooney - Web App Cloning Agent

An agentic system that automates web application replication, focusing on replicating Asana's Home, Projects, and Tasks pages with high fidelity.

## Project Structure

```
clooney-scaler/
├── agent/              # Agentic system for analysis and replication
├── backend/            # FastAPI backend with APIs and WebSockets
├── frontend/           # Next.js frontend application
├── .env.template       # Environment variables template
└── README.md          # This file
```

## Features

### Part A: Frontend Replication
- React/Next.js application with Tailwind CSS
- Home, Projects, and Tasks pages
- Pixel-perfect UI replication
- Visual testing setup with Playwright

### Part B: Backend Replication
- FastAPI REST API
- WebSocket support for real-time updates
- Database schema and migrations
- Comprehensive test cases
- OpenAPI specification

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL (or SQLite for development)
- OpenAI API key

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd clooney-scaler
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file from `.env.template`:
```bash
cp .env.template .env
# Edit .env and add your OpenAI API key
```

Run migrations:
```bash
alembic upgrade head
```

Start the backend server:
```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

Create `.env.local` file:
```bash
cp .env.template .env.local
# Add NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the frontend:
```bash
npm run dev
```

### 4. Running the Agent

```bash
cd agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py --target-url https://app.asana.com
```

## Usage

### Using the Agent

The agent analyzes the target web application and generates replication code:

```bash
python agent/main.py --target-url <url> --component frontend|backend|both
```

### Running Tests

Backend tests:
```bash
cd backend
pytest
```

Frontend visual tests:
```bash
cd frontend
npm run test:visual
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Evaluation Notes

This implementation focuses on:
- Home page: Dashboard with task overview
- Projects page: List and manage projects
- Tasks page: Create, edit, delete, and view tasks

The agent uses OpenAI to analyze the target application and generate replication code iteratively.

## License

MIT

