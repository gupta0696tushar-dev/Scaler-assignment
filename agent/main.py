"""
Clooney Agent - Web App Cloning Agent
Uses OpenAI to analyze and replicate web applications
"""
import os
import sys
import argparse
import json
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ClooneyAgent:
    """Agentic system for web application replication"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("AGENT_MODEL", "gpt-4")
        self.temperature = float(os.getenv("AGENT_TEMPERATURE", "0.3"))
        
    def analyze_web_app(self, target_url: str, component: str = "both") -> Dict:
        """
        Analyze target web application and generate replication plan
        """
        prompt = f"""
        You are an expert web application analyzer. Analyze the following web application:
        Target URL: {target_url}
        
        Focus on replicating:
        1. API/WebSocket interfaces (routes, schemas, validations)
        2. UI/UX elements (layout, styling, interactions)
        3. Data schema (based on API resources)
        
        For Asana specifically, focus on:
        - Home page: Dashboard with task overview, recent activity
        - Projects page: List projects, create/edit/delete projects, project details
        - Tasks page: Create/edit/delete tasks, task details, task assignments
        
        Component to replicate: {component}
        
        Provide a structured analysis in JSON format with:
        {{
            "api_endpoints": [
                {{"path": "...", "method": "...", "request_schema": {{}}, "response_schema": {{}}}}
            ],
            "websocket_messages": [
                {{"type": "...", "payload": {{}}}}
            ],
            "ui_components": [
                {{"page": "...", "components": [...], "styles": {{}}}}
            ],
            "data_schema": {{
                "tables": [
                    {{"name": "...", "columns": [...]}}
                ]
            }}
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert web application analyzer specializing in creating high-fidelity replicas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            
            content = response.choices[0].message.content
            # Try to extract JSON from response
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            
            return json.loads(content)
        except Exception as e:
            print(f"Error analyzing web app: {e}")
            return self._get_default_analysis()
    
    def generate_backend_code(self, analysis: Dict) -> str:
        """Generate backend code based on analysis"""
        prompt = f"""
        Generate FastAPI backend code based on this analysis:
        {json.dumps(analysis, indent=2)}
        
        Requirements:
        1. Create FastAPI routes matching the API endpoints
        2. Include request/response models using Pydantic
        3. Add WebSocket support for real-time updates
        4. Include database models using SQLAlchemy
        5. Add comprehensive validation and error handling
        6. Include test cases for edge cases (empty, null, long strings, special chars)
        
        Focus on:
        - Tasks: CRUD operations
        - Projects: CRUD operations
        - Home: Dashboard data aggregation
        
        Return only the Python code for main.py with all routes.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert Python/FastAPI developer."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return response.choices[0].message.content
    
    def generate_frontend_code(self, analysis: Dict) -> str:
        """Generate frontend code based on analysis"""
        prompt = f"""
        Generate Next.js/React frontend code with Tailwind CSS based on this analysis:
        {json.dumps(analysis, indent=2)}
        
        Requirements:
        1. Create pages for Home, Projects, and Tasks
        2. Use Tailwind CSS for styling (match exact colors, spacing, layout)
        3. Include all UI interactions (hover, click, forms)
        4. Connect to backend API
        5. Handle WebSocket connections for real-time updates
        
        Focus on pixel-perfect replication of:
        - Home page layout and components
        - Projects list and detail pages
        - Tasks list, create/edit forms, and detail view
        
        Return the code structure and key component files.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert React/Next.js developer specializing in pixel-perfect UI replication."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return response.choices[0].message.content
    
    def _get_default_analysis(self) -> Dict:
        """Fallback default analysis for Asana"""
        return {
            "api_endpoints": [
                {
                    "path": "/api/tasks",
                    "method": "GET",
                    "description": "List all tasks",
                    "request_schema": {"query_params": {"project_id": "optional"}},
                    "response_schema": {"tasks": "array"}
                },
                {
                    "path": "/api/tasks",
                    "method": "POST",
                    "description": "Create task",
                    "request_schema": {"name": "string", "project_id": "optional"},
                    "response_schema": {"task": "object"}
                },
                {
                    "path": "/api/projects",
                    "method": "GET",
                    "description": "List all projects",
                    "request_schema": {},
                    "response_schema": {"projects": "array"}
                }
            ],
            "websocket_messages": [
                {"type": "task_updated", "payload": {"task_id": "string", "changes": "object"}},
                {"type": "project_updated", "payload": {"project_id": "string", "changes": "object"}}
            ],
            "ui_components": [
                {"page": "home", "components": ["sidebar", "task_list", "recent_activity"]},
                {"page": "projects", "components": ["project_list", "project_card", "create_modal"]},
                {"page": "tasks", "components": ["task_list", "task_form", "task_detail"]}
            ],
            "data_schema": {
                "tables": [
                    {
                        "name": "projects",
                        "columns": [
                            {"name": "id", "type": "uuid", "primary_key": True},
                            {"name": "name", "type": "string"},
                            {"name": "description", "type": "text", "nullable": True},
                            {"name": "created_at", "type": "timestamp"}
                        ]
                    },
                    {
                        "name": "tasks",
                        "columns": [
                            {"name": "id", "type": "uuid", "primary_key": True},
                            {"name": "name", "type": "string"},
                            {"name": "description", "type": "text", "nullable": True},
                            {"name": "project_id", "type": "uuid", "foreign_key": "projects.id"},
                            {"name": "completed", "type": "boolean", "default": False},
                            {"name": "due_date", "type": "date", "nullable": True},
                            {"name": "created_at", "type": "timestamp"}
                        ]
                    }
                ]
            }
        }


def main():
    parser = argparse.ArgumentParser(description="Clooney - Web App Cloning Agent")
    parser.add_argument("--target-url", type=str, default="https://app.asana.com",
                       help="Target web application URL to replicate")
    parser.add_argument("--component", type=str, choices=["frontend", "backend", "both"],
                       default="both", help="Component to replicate")
    parser.add_argument("--output-dir", type=str, default="output",
                       help="Output directory for generated code")
    
    args = parser.parse_args()
    
    print("🤖 Clooney Agent - Starting analysis...")
    print(f"Target: {args.target_url}")
    print(f"Component: {args.component}")
    
    agent = ClooneyAgent()
    
    # Analyze web app
    print("\n📊 Analyzing web application...")
    analysis = agent.analyze_web_app(args.target_url, args.component)
    
    # Save analysis
    os.makedirs(args.output_dir, exist_ok=True)
    with open(f"{args.output_dir}/analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    print(f"✅ Analysis saved to {args.output_dir}/analysis.json")
    
    # Generate code
    if args.component in ["backend", "both"]:
        print("\n🔧 Generating backend code...")
        backend_code = agent.generate_backend_code(analysis)
        with open(f"{args.output_dir}/backend_code.txt", "w") as f:
            f.write(backend_code)
        print(f"✅ Backend code saved to {args.output_dir}/backend_code.txt")
    
    if args.component in ["frontend", "both"]:
        print("\n🎨 Generating frontend code...")
        frontend_code = agent.generate_frontend_code(analysis)
        with open(f"{args.output_dir}/frontend_code.txt", "w") as f:
            f.write(frontend_code)
        print(f"✅ Frontend code saved to {args.output_dir}/frontend_code.txt")
    
    print("\n✨ Analysis complete!")


if __name__ == "__main__":
    main()

