'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Task, Project } from '@/types'
import { format } from 'date-fns'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    project_id: '',
    completed: false,
    due_date: '',
  })

  useEffect(() => {
    fetchTasks()
    fetchProjects()
  }, [])

  const fetchTasks = async () => {
    try {
      const res = await fetch(`${API_URL}/api/tasks`)
      const data = await res.json()
      setTasks(data)
      setLoading(false)
    } catch (err) {
      console.error('Error fetching tasks:', err)
      setLoading(false)
    }
  }

  const fetchProjects = async () => {
    try {
      const res = await fetch(`${API_URL}/api/projects`)
      const data = await res.json()
      setProjects(data)
    } catch (err) {
      console.error('Error fetching projects:', err)
    }
  }

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const payload = {
        ...formData,
        project_id: formData.project_id || null,
        due_date: formData.due_date || null,
      }
      const res = await fetch(`${API_URL}/api/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      if (res.ok) {
        setShowModal(false)
        setFormData({
          name: '',
          description: '',
          project_id: '',
          completed: false,
          due_date: '',
        })
        fetchTasks()
      }
    } catch (err) {
      console.error('Error creating task:', err)
    }
  }

  const handleToggleComplete = async (task: Task) => {
    try {
      const res = await fetch(`${API_URL}/api/tasks/${task.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !task.completed }),
      })
      if (res.ok) {
        fetchTasks()
      }
    } catch (err) {
      console.error('Error updating task:', err)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this task?')) return
    try {
      const res = await fetch(`${API_URL}/api/tasks/${id}`, {
        method: 'DELETE',
      })
      if (res.ok) {
        fetchTasks()
      }
    } catch (err) {
      console.error('Error deleting task:', err)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-white border-r border-gray-200">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-primary">Clooney</h1>
        </div>
        <nav className="px-4">
          <Link href="/" className="block py-2 px-4 text-gray-700 hover:bg-gray-50 rounded">
            Home
          </Link>
          <Link href="/projects" className="block py-2 px-4 text-gray-700 hover:bg-gray-50 rounded">
            Projects
          </Link>
          <Link href="/tasks" className="block py-2 px-4 text-primary font-semibold bg-purple-50 rounded">
            Tasks
          </Link>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="ml-64 p-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold">Tasks</h2>
            <button
              onClick={() => setShowModal(true)}
              className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition"
            >
              + New Task
            </button>
          </div>

          {loading ? (
            <div className="text-center py-12">Loading...</div>
          ) : tasks.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-12 text-center">
              <p className="text-gray-500 mb-4">No tasks yet</p>
              <button
                onClick={() => setShowModal(true)}
                className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition"
              >
                Create your first task
              </button>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow">
              <div className="p-6">
                <ul className="space-y-3">
                  {tasks.map((task) => (
                    <li
                      key={task.id}
                      className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-primary transition"
                    >
                      <div className="flex items-center space-x-4 flex-1">
                        <input
                          type="checkbox"
                          checked={task.completed}
                          onChange={() => handleToggleComplete(task)}
                          className="w-5 h-5 text-primary rounded"
                        />
                        <div className="flex-1">
                          <Link href={`/tasks/${task.id}`}>
                            <span
                              className={`text-lg ${
                                task.completed
                                  ? 'line-through text-gray-500'
                                  : 'text-gray-900'
                              } hover:text-primary cursor-pointer`}
                            >
                              {task.name}
                            </span>
                          </Link>
                          {task.description && (
                            <p className="text-sm text-gray-600 mt-1">{task.description}</p>
                          )}
                          <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                            {task.due_date && (
                              <span>Due: {format(new Date(task.due_date), 'MMM d, yyyy')}</span>
                            )}
                            {task.created_at && (
                              <span>Created: {format(new Date(task.created_at), 'MMM d, yyyy')}</span>
                            )}
                          </div>
                        </div>
                      </div>
                      <button
                        onClick={() => handleDelete(task.id)}
                        className="text-red-500 hover:text-red-700 px-3 py-1 text-sm"
                      >
                        Delete
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Create Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-xl font-semibold mb-4">Create New Task</h3>
            <form onSubmit={handleCreate}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                  rows={3}
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Project</label>
                <select
                  value={formData.project_id}
                  onChange={(e) => setFormData({ ...formData, project_id: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                >
                  <option value="">None</option>
                  {projects.map((project) => (
                    <option key={project.id} value={project.id}>
                      {project.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Due Date</label>
                <input
                  type="date"
                  value={formData.due_date}
                  onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                />
              </div>
              <div className="flex items-center mb-4">
                <input
                  type="checkbox"
                  checked={formData.completed}
                  onChange={(e) => setFormData({ ...formData, completed: e.target.checked })}
                  className="w-4 h-4 text-primary rounded"
                />
                <label className="ml-2 text-sm">Completed</label>
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-purple-700"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

