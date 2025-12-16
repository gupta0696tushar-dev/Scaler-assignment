"""
FastAPI Backend for Clooney - Asana Replica
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
import uuid
from pydantic import BaseModel, Field, validator
import json

from database import SessionLocal, engine, Base
from models import Project, Task
from schemas import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    TaskCreate, TaskUpdate, TaskResponse,
    DashboardResponse
)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clooney API",
    description="Backend API for Asana replica",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connections manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Health check
@app.get("/")
async def root():
    return {"message": "Clooney API is running"}


# Projects endpoints
@app.get("/api/projects", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all projects"""
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects


@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, db: Session = Depends(get_db)):
    """Get project by ID"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.post("/api/projects", response_model=ProjectResponse, status_code=201)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Broadcast via WebSocket
    await manager.broadcast({
        "type": "project_created",
        "payload": ProjectResponse.model_validate(db_project).model_dump()
    })
    
    return db_project


@app.put("/api/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Update a project"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    
    # Broadcast via WebSocket
    await manager.broadcast({
        "type": "project_updated",
        "payload": ProjectResponse.model_validate(db_project).model_dump()
    })
    
    return db_project


@app.delete("/api/projects/{project_id}", status_code=204)
async def delete_project(project_id: str, db: Session = Depends(get_db)):
    """Delete a project"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    
    # Broadcast via WebSocket
    await manager.broadcast({
        "type": "project_deleted",
        "payload": {"project_id": project_id}
    })
    
    return None


# Tasks endpoints
@app.get("/api/tasks", response_model=List[TaskResponse])
async def list_tasks(
    project_id: Optional[str] = None,
    completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all tasks, optionally filtered by project"""
    query = db.query(Task)
    
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    tasks = query.offset(skip).limit(limit).all()
    return tasks


@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    """Get task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/api/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    # Validate project exists if project_id provided
    if task.project_id:
        project = db.query(Project).filter(Project.id == task.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
    
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Broadcast via WebSocket
    await manager.broadcast({
        "type": "task_created",
        "payload": TaskResponse.model_validate(db_task).model_dump()
    })
    
    return db_task


@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update a task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    
    # Validate project exists if project_id is being updated
    if "project_id" in update_data and update_data["project_id"]:
        project = db.query(Project).filter(Project.id == update_data["project_id"]).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    
    # Broadcast via WebSocket
    await manager.broadcast({
        "type": "task_updated",
        "payload": TaskResponse.model_validate(db_task).model_dump()
    })
    
    return db_task


@app.delete("/api/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    """Delete a task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    
    # Broadcast via WebSocket
    await manager.broadcast({
        "type": "task_deleted",
        "payload": {"task_id": task_id}
    })
    
    return None


# Dashboard endpoint
@app.get("/api/dashboard", response_model=DashboardResponse)
async def get_dashboard(db: Session = Depends(get_db)):
    """Get dashboard data for home page"""
    total_projects = db.query(Project).count()
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.completed == True).count()
    recent_tasks = db.query(Task).order_by(Task.created_at.desc()).limit(10).all()
    recent_projects = db.query(Project).order_by(Project.created_at.desc()).limit(5).all()
    
    return DashboardResponse(
        total_projects=total_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=total_tasks - completed_tasks,
        recent_tasks=[TaskResponse.model_validate(t) for t in recent_tasks],
        recent_projects=[ProjectResponse.model_validate(p) for p in recent_projects]
    )


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back or handle client messages
            await websocket.send_json({"type": "ack", "message": "Received"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

