'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Project } from '@/types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [formData, setFormData] = useState({ name: '', description: '' })

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const res = await fetch(`${API_URL}/api/projects`)
      const data = await res.json()
      setProjects(data)
      setLoading(false)
    } catch (err) {
      console.error('Error fetching projects:', err)
      setLoading(false)
    }
  }

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch(`${API_URL}/api/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      if (res.ok) {
        setShowModal(false)
        setFormData({ name: '', description: '' })
        fetchProjects()
      }
    } catch (err) {
      console.error('Error creating project:', err)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this project?')) return
    try {
      const res = await fetch(`${API_URL}/api/projects/${id}`, {
        method: 'DELETE',
      })
      if (res.ok) {
        fetchProjects()
      }
    } catch (err) {
      console.error('Error deleting project:', err)
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
          <Link href="/projects" className="block py-2 px-4 text-primary font-semibold bg-purple-50 rounded">
            Projects
          </Link>
          <Link href="/tasks" className="block py-2 px-4 text-gray-700 hover:bg-gray-50 rounded">
            Tasks
          </Link>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="ml-64 p-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold">Projects</h2>
            <button
              onClick={() => setShowModal(true)}
              className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition"
            >
              + New Project
            </button>
          </div>

          {loading ? (
            <div className="text-center py-12">Loading...</div>
          ) : projects.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-12 text-center">
              <p className="text-gray-500 mb-4">No projects yet</p>
              <button
                onClick={() => setShowModal(true)}
                className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition"
              >
                Create your first project
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {projects.map((project) => (
                <div key={project.id} className="bg-white rounded-lg shadow p-6">
                  <div className="flex justify-between items-start mb-4">
                    <Link href={`/projects/${project.id}`}>
                      <h3 className="text-xl font-semibold text-primary hover:underline">
                        {project.name}
                      </h3>
                    </Link>
                    <button
                      onClick={() => handleDelete(project.id)}
                      className="text-red-500 hover:text-red-700 text-sm"
                    >
                      Delete
                    </button>
                  </div>
                  {project.description && (
                    <p className="text-gray-600 mb-4">{project.description}</p>
                  )}
                  <Link
                    href={`/projects/${project.id}`}
                    className="text-primary hover:underline text-sm"
                  >
                    View Details →
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Create Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-xl font-semibold mb-4">Create New Project</h3>
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

