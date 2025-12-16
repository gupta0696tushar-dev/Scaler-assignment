# Setup Instructions - Clooney Web App Cloning Agent

## Quick Start Guide

This guide will help you set up and run the Clooney project for your interview evaluation.

## Prerequisites

Before starting, ensure you have:
- Python 3.9 or higher
- Node.js 18 or higher
- PostgreSQL (optional, SQLite works for development)
- OpenAI API key

## Step-by-Step Setup

### 1. Clone and Navigate

```bash
cd clooney-scaler
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from env.template in root)
# Add your OpenAI API key and database URL
# For SQLite (quick start):
# DATABASE_URL=sqlite:///./clooney.db

# Run the backend server
uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Frontend Setup

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local file
# Add: NEXT_PUBLIC_API_URL=http://localhost:8000

# Start the frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Running the Agent

Open another terminal window:

```bash
# Navigate to agent directory
cd agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the agent
python main.py --target-url https://app.asana.com --component both
```

## Running Tests

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Visual Tests

```bash
cd frontend
npm run test:visual
```

## Environment Variables

Create `.env` files in respective directories:

**Backend `.env`:**
```
OPENAI_API_KEY=your_key_here
DATABASE_URL=sqlite:///./clooney.db
```

**Frontend `.env.local`:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Troubleshooting

### Backend Issues
- If port 8000 is in use, change it: `uvicorn main:app --reload --port 8001`
- For SQLite, ensure write permissions in the backend directory
- Check that all dependencies are installed: `pip list`

### Frontend Issues
- Clear `.next` folder: `rm -rf .next` (or `rmdir /s .next` on Windows)
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check that backend is running on the correct port

### Agent Issues
- Verify OpenAI API key is set correctly
- Check API key has sufficient credits
- Ensure internet connection for API calls

## Project Structure

```
clooney-scaler/
├── agent/              # Agentic system (OpenAI-based)
│   ├── main.py        # Agent entry point
│   └── requirements.txt
├── backend/            # FastAPI backend
│   ├── main.py        # API routes
│   ├── models.py      # Database models
│   ├── schemas.py     # Pydantic schemas
│   ├── database.py    # DB configuration
│   ├── api.yml        # OpenAPI spec
│   ├── schema.sql     # SQL schema
│   └── tests/         # Test cases
├── frontend/          # Next.js frontend
│   ├── app/           # Pages and components
│   ├── tests/         # Visual tests
│   └── package.json
└── README.md
```

## Key Features Implemented

### Backend (Part B)
✅ REST API endpoints for Projects and Tasks
✅ WebSocket support for real-time updates
✅ Comprehensive test cases with edge case coverage
✅ OpenAPI specification (api.yml)
✅ Database schema (schema.sql)
✅ Request/response validation
✅ Error handling

### Frontend (Part A)
✅ Home page with dashboard
✅ Projects page (list, create, edit, delete)
✅ Tasks page (list, create, edit, delete)
✅ Tailwind CSS styling
✅ Visual testing setup with Playwright
✅ CSS property assertions

### Agent
✅ OpenAI integration for web app analysis
✅ Code generation for frontend and backend
✅ Structured analysis output

## Evaluation Notes

- The agent uses OpenAI GPT-4 to analyze Asana and generate replication code
- Backend includes exhaustive test cases covering edge cases (empty, null, long strings, special chars)
- Frontend uses Asana-like color scheme (#3a258e primary color)
- All components are minimal but functional, matching ~8 hours of development effort

## Support

If you encounter any issues during setup, check:
1. All prerequisites are installed
2. Environment variables are set correctly
3. Ports 3000 and 8000 are available
4. Dependencies are installed in correct virtual environments

