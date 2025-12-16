"""
Comprehensive test cases for API endpoints
Testing edge cases: empty, null, long strings, special characters
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestProjectsAPI:
    """Test cases for Projects endpoints"""
    
    def test_create_project_valid(self):
        """Test creating project with valid data"""
        response = client.post("/api/projects", json={
            "name": "Test Project",
            "description": "Test description"
        })
        assert response.status_code == 201
        assert response.json()["name"] == "Test Project"
    
    def test_create_project_empty_name(self):
        """Test creating project with empty name"""
        response = client.post("/api/projects", json={
            "name": "",
            "description": "Test"
        })
        assert response.status_code == 422  # Validation error
    
    def test_create_project_null_name(self):
        """Test creating project with null name"""
        response = client.post("/api/projects", json={
            "name": None,
            "description": "Test"
        })
        assert response.status_code == 422
    
    def test_create_project_long_name(self):
        """Test creating project with very long name"""
        long_name = "a" * 201  # Exceeds max_length=200
        response = client.post("/api/projects", json={
            "name": long_name,
            "description": "Test"
        })
        assert response.status_code == 422
    
    def test_create_project_special_characters(self):
        """Test creating project with special characters"""
        response = client.post("/api/projects", json={
            "name": "Project !@#$%^&*()_+-=[]{}|;':\",./<>?",
            "description": "Test"
        })
        assert response.status_code == 201
    
    def test_create_project_long_description(self):
        """Test creating project with very long description"""
        long_desc = "a" * 1001  # Exceeds max_length=1000
        response = client.post("/api/projects", json={
            "name": "Test Project",
            "description": long_desc
        })
        assert response.status_code == 422
    
    def test_get_project_not_found(self):
        """Test getting non-existent project"""
        response = client.get("/api/projects/non-existent-id")
        assert response.status_code == 404
    
    def test_update_project_empty_name(self):
        """Test updating project with empty name"""
        # Create project first
        create_response = client.post("/api/projects", json={
            "name": "Original Name",
            "description": "Test"
        })
        project_id = create_response.json()["id"]
        
        # Try to update with empty name
        response = client.put(f"/api/projects/{project_id}", json={
            "name": ""
        })
        assert response.status_code == 422
    
    def test_delete_project(self):
        """Test deleting a project"""
        # Create project
        create_response = client.post("/api/projects", json={
            "name": "To Delete",
            "description": "Test"
        })
        project_id = create_response.json()["id"]
        
        # Delete project
        response = client.delete(f"/api/projects/{project_id}")
        assert response.status_code == 204
        
        # Verify deleted
        get_response = client.get(f"/api/projects/{project_id}")
        assert get_response.status_code == 404


class TestTasksAPI:
    """Test cases for Tasks endpoints"""
    
    def test_create_task_valid(self):
        """Test creating task with valid data"""
        response = client.post("/api/tasks", json={
            "name": "Test Task",
            "description": "Test description",
            "completed": False
        })
        assert response.status_code == 201
        assert response.json()["name"] == "Test Task"
    
    def test_create_task_empty_name(self):
        """Test creating task with empty name"""
        response = client.post("/api/tasks", json={
            "name": "",
            "description": "Test"
        })
        assert response.status_code == 422
    
    def test_create_task_null_name(self):
        """Test creating task with null name"""
        response = client.post("/api/tasks", json={
            "name": None,
            "description": "Test"
        })
        assert response.status_code == 422
    
    def test_create_task_long_name(self):
        """Test creating task with very long name"""
        long_name = "a" * 201
        response = client.post("/api/tasks", json={
            "name": long_name,
            "description": "Test"
        })
        assert response.status_code == 422
    
    def test_create_task_special_characters(self):
        """Test creating task with special characters"""
        response = client.post("/api/tasks", json={
            "name": "Task !@#$%^&*()_+-=[]{}|;':\",./<>?",
            "description": "Test"
        })
        assert response.status_code == 201
    
    def test_create_task_with_invalid_project_id(self):
        """Test creating task with non-existent project_id"""
        response = client.post("/api/tasks", json={
            "name": "Test Task",
            "project_id": "non-existent-project-id"
        })
        assert response.status_code == 404
    
    def test_create_task_with_valid_project_id(self):
        """Test creating task with valid project_id"""
        # Create project first
        project_response = client.post("/api/projects", json={
            "name": "Test Project",
            "description": "Test"
        })
        project_id = project_response.json()["id"]
        
        # Create task with project_id
        task_response = client.post("/api/tasks", json={
            "name": "Test Task",
            "project_id": project_id
        })
        assert task_response.status_code == 201
        assert task_response.json()["project_id"] == project_id
    
    def test_list_tasks_filter_by_project(self):
        """Test listing tasks filtered by project"""
        # Create project
        project_response = client.post("/api/projects", json={
            "name": "Filter Project",
            "description": "Test"
        })
        project_id = project_response.json()["id"]
        
        # Create tasks
        client.post("/api/tasks", json={
            "name": "Task 1",
            "project_id": project_id
        })
        client.post("/api/tasks", json={
            "name": "Task 2",
            "project_id": project_id
        })
        client.post("/api/tasks", json={
            "name": "Task 3",
            "project_id": None
        })
        
        # Filter by project
        response = client.get(f"/api/tasks?project_id={project_id}")
        assert response.status_code == 200
        assert len(response.json()) == 2
    
    def test_list_tasks_filter_by_completed(self):
        """Test listing tasks filtered by completed status"""
        # Create tasks
        client.post("/api/tasks", json={
            "name": "Completed Task",
            "completed": True
        })
        client.post("/api/tasks", json={
            "name": "Pending Task",
            "completed": False
        })
        
        # Filter completed
        response = client.get("/api/tasks?completed=true")
        assert response.status_code == 200
        assert all(task["completed"] for task in response.json())
        
        # Filter pending
        response = client.get("/api/tasks?completed=false")
        assert response.status_code == 200
        assert all(not task["completed"] for task in response.json())
    
    def test_update_task_not_found(self):
        """Test updating non-existent task"""
        response = client.put("/api/tasks/non-existent-id", json={
            "name": "Updated Name"
        })
        assert response.status_code == 404
    
    def test_delete_task(self):
        """Test deleting a task"""
        # Create task
        create_response = client.post("/api/tasks", json={
            "name": "To Delete",
            "description": "Test"
        })
        task_id = create_response.json()["id"]
        
        # Delete task
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 204
        
        # Verify deleted
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404


class TestDashboardAPI:
    """Test cases for Dashboard endpoint"""
    
    def test_get_dashboard(self):
        """Test getting dashboard data"""
        # Create some data
        project_response = client.post("/api/projects", json={
            "name": "Dashboard Project",
            "description": "Test"
        })
        project_id = project_response.json()["id"]
        
        client.post("/api/tasks", json={
            "name": "Completed Task",
            "project_id": project_id,
            "completed": True
        })
        client.post("/api/tasks", json={
            "name": "Pending Task",
            "project_id": project_id,
            "completed": False
        })
        
        response = client.get("/api/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "total_projects" in data
        assert "total_tasks" in data
        assert "completed_tasks" in data
        assert "pending_tasks" in data
        assert "recent_tasks" in data
        assert "recent_projects" in data

