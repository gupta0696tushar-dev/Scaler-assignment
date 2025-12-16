# Quick Start Guide - Run Clooney on Localhost

This guide will help you run the Clooney application on your local machine in just a few minutes.

## Prerequisites Check

Before starting, make sure you have:
- ✅ Python 3.9 or higher (check: `python --version`)
- ✅ Node.js 18 or higher (check: `node --version`)
- ✅ OpenAI API key (optional for basic testing, required for agent)

---

## Step 1: Backend Setup (Terminal 1)

### 1.1 Navigate to Backend Directory
```bash
cd backend
```

### 1.2 Create Virtual Environment
```bash
python -m venv venv
```

### 1.3 Activate Virtual Environment

**⚠️ IMPORTANT for Windows Users:**
If you get a PowerShell execution policy error, **use Command Prompt instead of PowerShell** (recommended for Windows).

**On Windows (Command Prompt - RECOMMENDED):**
```cmd
venv\Scripts\activate.bat
```

**On Windows (PowerShell - if you get errors, use Command Prompt instead):**
```powershell
# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 1.4 Install Dependencies
```bash
pip install -r requirements.txt
```

### 1.5 Create Environment File
Create a file named `.env` in the `backend` folder with this content:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./clooney.db
```

**Note:** For quick testing, you can use a dummy key. The backend will work without OpenAI for basic operations.

### 1.6 Start Backend Server
```bash
uvicorn main:app --reload --port 8000
```

**Success indicators:**
- You should see: `INFO: Uvicorn running on http://127.0.0.1:8000`
- Open http://localhost:8000/docs in your browser to see the API documentation

**Keep this terminal open!** The backend needs to keep running.

---

## Step 2: Frontend Setup (Terminal 2)

Open a **NEW terminal window** (keep the backend running in Terminal 1).

### 2.1 Navigate to Frontend Directory
```bash
cd frontend
```

### 2.2 Install Dependencies

**⚠️ If you get PowerShell execution policy error, use Command Prompt instead:**

**In Command Prompt (cmd):**
```cmd
cd C:\Users\Admin\Desktop\py-replica\clooney-scaler\frontend
npm install
```

**Or fix PowerShell execution policy:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
npm install
```

This may take a few minutes the first time.

### 2.3 Create Environment File
Create a file named `.env.local` in the `frontend` folder with this content:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2.4 Start Frontend Server
```bash
npm run dev
```

**Success indicators:**
- You should see: `- Local: http://localhost:3000`
- The frontend will automatically open in your browser

**Keep this terminal open too!** The frontend needs to keep running.

---

## Step 3: Access the Application

### Open in Browser
Navigate to: **http://localhost:3000**

You should see:
- **Home Page** - Dashboard with statistics
- **Projects Page** - Create and manage projects
- **Tasks Page** - Create and manage tasks

### Test the Application

1. **Create a Project:**
   - Click "Projects" in the sidebar
   - Click "+ New Project"
   - Enter a name and description
   - Click "Create"

2. **Create a Task:**
   - Click "Tasks" in the sidebar
   - Click "+ New Task"
   - Enter a task name
   - Optionally select a project
   - Click "Create"

3. **View Dashboard:**
   - Click "Home" in the sidebar
   - See your statistics and recent items

---

## Quick Troubleshooting

### Backend Issues

**Problem:** `uvicorn: command not found`
**Solution:** Make sure virtual environment is activated and dependencies are installed:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

**Problem:** Port 8000 already in use
**Solution:** Use a different port:
```bash
uvicorn main:app --reload --port 8001
```
Then update frontend `.env.local` to: `NEXT_PUBLIC_API_URL=http://localhost:8001`

**Problem:** Database errors
**Solution:** Delete `clooney.db` file in backend folder and restart:
```bash
# Stop server (Ctrl+C)
# Delete database file
del clooney.db  # Windows
# or
rm clooney.db   # macOS/Linux
# Restart server
uvicorn main:app --reload --port 8000
```

### Frontend Issues

**Problem:** `npm: command not found`
**Solution:** Install Node.js from https://nodejs.org/

**Problem:** Port 3000 already in use
**Solution:** Next.js will automatically use port 3001, 3002, etc.

**Problem:** Cannot connect to backend
**Solution:** 
- Make sure backend is running on port 8000
- Check `.env.local` has correct URL: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Check browser console for errors (F12)

**Problem:** Dependencies installation fails
**Solution:** Clear and reinstall:
```bash
rmdir /s node_modules  # Windows
# or
rm -rf node_modules    # macOS/Linux
npm install
```

### General Issues

**Problem:** Changes not reflecting
**Solution:** 
- Backend: Restart server (Ctrl+C, then run uvicorn again)
- Frontend: Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)

**Problem:** Module not found errors
**Solution:** Make sure you're in the correct directory and virtual environment is activated

---

## Verify Everything is Working

### Check Backend
1. Open http://localhost:8000/docs
2. You should see Swagger API documentation
3. Try the "GET /api/projects" endpoint - should return `[]`

### Check Frontend
1. Open http://localhost:3000
2. You should see the Home page with sidebar
3. Click around - pages should load without errors

### Check Database
1. Look for `clooney.db` file in `backend` folder
2. It should be created automatically when you start the backend

---

## Running Both Servers

You need **TWO terminal windows** running simultaneously:

**Terminal 1 (Backend):**
```
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```
cd frontend
npm run dev
```

Both should be running for the app to work!

---

## Next Steps

Once everything is running:

1. **Explore the API:** Visit http://localhost:8000/docs
2. **Test Features:** Create projects and tasks through the UI
3. **Check Database:** The SQLite database is in `backend/clooney.db`
4. **View Logs:** Check terminal windows for any errors

---

## Optional: Run the Agent

If you want to test the agent component (requires OpenAI API key):

**Terminal 3:**
```bash
cd agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py --target-url https://app.asana.com --component both
```

---

## Summary

✅ **Backend running on:** http://localhost:8000
✅ **Frontend running on:** http://localhost:3000
✅ **API Docs:** http://localhost:8000/docs

**That's it!** Your Clooney application should now be running on localhost. 🎉

