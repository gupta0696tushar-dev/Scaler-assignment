# Fix PowerShell Execution Policy - Complete Guide

If you're getting errors like:
- `cannot be loaded because running scripts is disabled on this system`
- This affects both Python (`venv\Scripts\activate`) and npm

## 🎯 BEST SOLUTION: Use Command Prompt

**Command Prompt (cmd) doesn't have execution policy restrictions!**

### For Python/Backend:
```cmd
# Open Command Prompt (Win + R, type "cmd")
cd C:\Users\Admin\Desktop\py-replica\clooney-scaler\backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

### For Node.js/Frontend:
```cmd
# Open Command Prompt
cd C:\Users\Admin\Desktop\py-replica\clooney-scaler\frontend
npm install
npm run dev
```

**That's it! No execution policy issues in Command Prompt.**

---

## Alternative: Fix PowerShell Execution Policy

If you prefer PowerShell, fix it permanently:

### Option 1: For Current User Only (Safest)
```powershell
# Run PowerShell (not as admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Option 2: For All Users (Requires Admin)
```powershell
# Right-click PowerShell → Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```

### Option 3: Bypass for Current Session Only
```powershell
# Run this each time you open PowerShell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

---

## Complete Setup Using Command Prompt (Recommended)

### Terminal 1 - Backend:
```cmd
cd C:\Users\Admin\Desktop\py-replica\clooney-scaler\backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt

# Create .env file with:
# OPENAI_API_KEY=your_key
# DATABASE_URL=sqlite:///./clooney.db

uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend:
```cmd
cd C:\Users\Admin\Desktop\py-replica\clooney-scaler\frontend
npm install

# Create .env.local file with:
# NEXT_PUBLIC_API_URL=http://localhost:8000

npm run dev
```

---

## Verify Execution Policy

Check current policy:
```powershell
Get-ExecutionPolicy
```

Common values:
- `Restricted` - Scripts blocked (your current issue)
- `RemoteSigned` - Local scripts allowed, downloaded scripts need signature
- `Unrestricted` - All scripts allowed (less secure)

---

## Why This Happens

Windows PowerShell has execution policies to prevent malicious scripts. By default, it's set to `Restricted` which blocks all scripts.

**Command Prompt doesn't have this restriction**, which is why it's the easiest solution for development.

---

## Summary

✅ **Easiest:** Use Command Prompt (cmd) - no configuration needed
✅ **Permanent Fix:** Change execution policy to `RemoteSigned` for CurrentUser
✅ **Temporary:** Bypass for current session only

**Recommendation:** Use Command Prompt for Python/Node.js development on Windows. It's simpler and avoids all these issues!

