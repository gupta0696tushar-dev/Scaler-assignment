export interface Project {
  id: string
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface Task {
  id: string
  name: string
  description?: string
  project_id?: string
  completed: boolean
  due_date?: string
  created_at: string
  updated_at: string
}

export interface DashboardResponse {
  total_projects: number
  total_tasks: number
  completed_tasks: number
  pending_tasks: number
  recent_tasks: Task[]
  recent_projects: Project[]
}

