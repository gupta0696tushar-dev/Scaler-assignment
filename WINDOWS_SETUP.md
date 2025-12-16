# Windows Setup Guide - Fixing PowerShell Execution Policy

If you're getting the error: "running scripts is disabled on this system" for Python or npm, here are several solutions:

## ⚠️ QUICK FIX: Use Command Prompt Instead

**The easiest solution is to use Command Prompt (cmd) instead of PowerShell for everything.**

Command Prompt doesn't have execution policy restrictions, so all commands work immediately.

## Solution 1: Use Command Prompt (Easiest)

Instead of PowerShell, use **Command Prompt** (cmd):

1. Open **Command Prompt** (not PowerShell)
2. Navigate to backend:
   ```cmd
   cd backend
   ```
3. Activate virtual environment:
   ```cmd
   venv\Scripts\activate.bat
   ```
   or
   ```cmd
   myenv\Scripts\activate.bat
   ```

This bypasses PowerShell entirely and works immediately.

---

## Solution 2: Change PowerShell Execution Policy (Recommended)

Run PowerShell **as Administrator** and execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```powershell
.\venv\Scripts\activate
```

**Note:** This allows scripts to run for your user account only (safe).

---

## Solution 3: Bypass for Current Session Only

If you don't want to change the policy permanently, run this in PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

Then activate:
```powershell
.\venv\Scripts\activate
```

**Note:** This only works for the current PowerShell session.

---

## Solution 4: Use Direct Python Path

Instead of activating, use the full path to Python:

```powershell
# Instead of activating, use:
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

---

## Quick Fix Commands

### For Backend Setup (PowerShell):

```powershell
# Navigate to backend
cd backend

# Create venv
python -m venv venv

# Option A: Use Command Prompt instead
# Open cmd and run: venv\Scripts\activate.bat

# Option B: Change execution policy (run as admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Option C: Bypass for this session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (manually or use notepad)
# Then run:
uvicorn main:app --reload --port 8000
```

---

## Recommended Approach

**For Windows users, I recommend using Command Prompt (cmd) instead of PowerShell** for Python virtual environments:

1. Open **Command Prompt** (Win + R, type `cmd`)
2. Navigate to your project:
   ```cmd
   cd C:\Users\Admin\Desktop\py-replica\clooney-scaler\backend
   ```
3. Create and activate:
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```
4. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

This avoids all PowerShell execution policy issues!

---

## Fixing npm in PowerShell

If you're getting npm errors in PowerShell, use Command Prompt:

**In Command Prompt:**
```cmd
cd C:\Users\Admin\Desktop\py-replica\clooney-scaler\frontend
npm install
npm run dev
```

**Or fix PowerShell execution policy permanently:**
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```

**Or bypass for current session:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
npm install
```

---

## Verify It's Working

After activation, you should see `(venv)` at the start of your prompt:

```
(venv) C:\Users\Admin\Desktop\py-replica\clooney-scaler\backend>
```

If you see this, you're good to go! 🎉

