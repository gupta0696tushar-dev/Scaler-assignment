# Interview Preparation Guide - Clooney Project

## Project Overview

**Clooney** is an agentic web application cloning system that replicates Asana's Home, Projects, and Tasks pages. The system uses OpenAI LLM to analyze and generate replication code for both frontend and backend components.

## Architecture

### Three Main Components

1. **Agent** (`/agent`)
   - Uses OpenAI GPT-4 to analyze target web applications
   - Generates structured analysis (API endpoints, UI components, data schema)
   - Produces replication code for frontend and backend

2. **Backend** (`/backend`)
   - FastAPI REST API
   - WebSocket support for real-time updates
   - SQLAlchemy ORM with SQLite/PostgreSQL
   - Comprehensive test suite with edge case coverage
   - OpenAPI specification (api.yml)
   - Database schema (schema.sql)

3. **Frontend** (`/frontend`)
   - Next.js 14 with React
   - Tailwind CSS for styling
   - Three main pages: Home, Projects, Tasks
   - Visual testing with Playwright
   - CSS property assertions

## Key Features Implemented

### Backend (Part B) ✅
- **REST API Endpoints:**
  - Projects: GET, POST, PUT, DELETE
  - Tasks: GET, POST, PUT, DELETE
  - Dashboard: GET (aggregated data)
  
- **WebSocket:** Real-time updates for project/task changes

- **Test Coverage:**
  - Empty values, null values
  - Very long strings (exceeding max_length)
  - Special characters
  - Invalid project_id references
  - Filtering by project_id and completed status

- **Validation:**
  - Pydantic schemas for request/response validation
  - Field-level validation (min_length, max_length)
  - Custom validators for edge cases

### Frontend (Part A) ✅
- **Home Page:**
  - Dashboard with stats (total projects, tasks, completed, pending)
  - Recent tasks list
  - Recent projects grid
  
- **Projects Page:**
  - List all projects
  - Create new project (modal)
  - Delete project
  - View project details (navigable)

- **Tasks Page:**
  - List all tasks
  - Create new task (modal with project selection)
  - Toggle task completion
  - Delete task
  - Filter by project (via API)

- **Styling:**
  - Asana-like color scheme (#3a258e primary)
  - Responsive layout
  - Sidebar navigation
  - Modern UI components

### Agent ✅
- Analyzes target web application
- Generates structured JSON analysis
- Produces backend code (FastAPI)
- Produces frontend code (Next.js/React)

## Technical Decisions

### Why SQLite for Development?
- Quick setup, no external dependencies
- Easy to reset for testing
- Can switch to PostgreSQL for production

### Why FastAPI?
- Modern async support
- Automatic OpenAPI generation
- Type validation with Pydantic
- WebSocket support built-in

### Why Next.js?
- Server-side rendering capability
- File-based routing
- Built-in optimizations
- TypeScript support

### Why OpenAI GPT-4?
- Best reasoning capabilities for analysis
- Can understand complex web app structures
- Generates production-ready code

## Project Structure

```
clooney-scaler/
├── agent/
│   ├── main.py              # Agent entry point
│   └── requirements.txt      # OpenAI, python-dotenv
├── backend/
│   ├── main.py              # FastAPI app with all routes
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # DB configuration
│   ├── api.yml              # OpenAPI 3.0 spec
│   ├── schema.sql           # SQL schema
│   ├── tests/
│   │   └── test_api.py      # Comprehensive test cases
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Home page
│   │   ├── projects/
│   │   │   └── page.tsx     # Projects page
│   │   └── tasks/
│   │       └── page.tsx     # Tasks page
│   ├── tests/
│   │   └── visual.spec.ts   # Playwright visual tests
│   └── package.json
├── README.md                # Project overview
├── SETUP.md                 # Detailed setup instructions
└── env.template             # Environment variables template
```

## How to Run (Quick Reference)

### 1. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
# Create .env with OPENAI_API_KEY and DATABASE_URL
uvicorn main:app --reload --port 8000
```

### 2. Frontend
```bash
cd frontend
npm install
# Create .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

### 3. Agent
```bash
cd agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py --target-url https://app.asana.com --component both
```

## Evaluation Criteria Coverage

### ✅ Part A: Frontend
- [x] React/Next.js & Tailwind
- [x] Visual testing setup (Playwright)
- [x] CSS property assertions
- [x] Home, Projects, Tasks pages
- [x] Add/Edit/Delete functionality

### ✅ Part B: Backend
- [x] FastAPI with Python
- [x] OpenAPI specs (api.yml)
- [x] schema.sql
- [x] Exhaustive test cases
- [x] WebSocket support
- [x] Edge case testing

### ✅ Agent
- [x] OpenAI LLM integration
- [x] Iterative analysis
- [x] Code generation

### ✅ Documentation
- [x] Clear setup instructions
- [x] README with overview
- [x] SETUP.md with detailed steps
- [x] env.template for configuration

## Common Interview Questions & Answers

### Q: How does the agent work?
**A:** The agent uses OpenAI GPT-4 to analyze the target web application. It sends structured prompts asking for API endpoints, UI components, and data schemas. The LLM returns JSON analysis which is then used to generate replication code for both frontend and backend.

### Q: Why did you choose this architecture?
**A:** 
- **Agent:** Separated to allow independent iteration and improvement
- **Backend:** FastAPI for modern async support and automatic API docs
- **Frontend:** Next.js for SSR and better performance
- **Database:** SQLite for dev simplicity, PostgreSQL-ready for production

### Q: How do you handle edge cases?
**A:** The test suite (`backend/tests/test_api.py`) covers:
- Empty strings (should fail validation)
- Null values (handled appropriately)
- Very long strings (exceeding max_length)
- Special characters (accepted if valid)
- Invalid foreign keys (404 errors)
- Missing required fields (422 validation errors)

### Q: How would you improve this?
**A:**
1. **Agent:** Add browser automation (Playwright) to actually scrape the target site
2. **Frontend:** Add more visual tests with pixel-perfect comparisons
3. **Backend:** Add authentication/authorization
4. **Testing:** Add integration tests and E2E tests
5. **Performance:** Add caching, pagination, database indexing

### Q: What challenges did you face?
**A:**
1. **Pydantic v2 compatibility:** Had to update `orm_mode` to `from_attributes` and `from_orm` to `model_validate`
2. **WebSocket broadcasting:** Implemented connection manager to handle multiple clients
3. **Type safety:** Used TypeScript for frontend, Pydantic for backend
4. **Time constraints:** Focused on core features matching ~8 hours of work

### Q: How do you ensure pixel-perfect replication?
**A:**
- Visual testing with Playwright captures screenshots
- CSS property assertions verify exact color values (e.g., #3a258e)
- Tailwind config matches Asana's color scheme
- Dynamic content masking prevents false test failures

## Git Setup

Repository is initialized with:
- **User:** gupta0696tushar-dev
- **Email:** gupta0696tushar@gmail.com
- **Initial commit:** Complete project structure

To push to remote:
```bash
git remote add origin <your-repo-url>
git push -u origin master
```

## Environment Variables

**Backend `.env`:**
```
OPENAI_API_KEY=your_key_here
DATABASE_URL=sqlite:///./clooney.db
```

**Frontend `.env.local`:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing

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

## API Endpoints Summary

- `GET /api/projects` - List projects
- `POST /api/projects` - Create project
- `GET /api/projects/{id}` - Get project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project
- `GET /api/tasks` - List tasks (filterable)
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `GET /api/dashboard` - Dashboard data
- `WS /ws` - WebSocket connection

## Final Notes

- **Minimal but complete:** Matches ~8 hours of skilled developer work
- **Production-ready structure:** Can be extended easily
- **Well-documented:** Clear setup and usage instructions
- **Tested:** Comprehensive test coverage
- **Modern stack:** Latest versions of frameworks

Good luck with your interview! 🚀

