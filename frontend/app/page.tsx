'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { DashboardResponse } from '@/types'
import { format } from 'date-fns'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_URL}/api/dashboard`)
      .then(res => res.json())
      .then(data => {
        setDashboard(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching dashboard:', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-white border-r border-gray-200">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-primary">Clooney</h1>
        </div>
        <nav className="px-4">
          <Link href="/" className="block py-2 px-4 text-primary font-semibold bg-purple-50 rounded">
            Home
          </Link>
          <Link href="/projects" className="block py-2 px-4 text-gray-700 hover:bg-gray-50 rounded">
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
          <h2 className="text-3xl font-bold mb-8">Home</h2>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-sm text-gray-600 mb-2">Total Projects</div>
              <div className="text-3xl font-bold text-primary">
                {dashboard?.total_projects || 0}
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-sm text-gray-600 mb-2">Total Tasks</div>
              <div className="text-3xl font-bold text-primary">
                {dashboard?.total_tasks || 0}
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-sm text-gray-600 mb-2">Completed</div>
              <div className="text-3xl font-bold text-green-600">
                {dashboard?.completed_tasks || 0}
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-sm text-gray-600 mb-2">Pending</div>
              <div className="text-3xl font-bold text-orange-600">
                {dashboard?.pending_tasks || 0}
              </div>
            </div>
          </div>

          {/* Recent Tasks */}
          <div className="bg-white rounded-lg shadow mb-8">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-xl font-semibold">Recent Tasks</h3>
            </div>
            <div className="p-6">
              {dashboard?.recent_tasks && dashboard.recent_tasks.length > 0 ? (
                <ul className="space-y-4">
                  {dashboard.recent_tasks.map((task) => (
                    <li key={task.id} className="flex items-center justify-between py-2 border-b border-gray-100">
                      <div className="flex items-center space-x-3">
                        <input
                          type="checkbox"
                          checked={task.completed}
                          readOnly
                          className="w-5 h-5 text-primary rounded"
                        />
                        <span className={task.completed ? 'line-through text-gray-500' : ''}>
                          {task.name}
                        </span>
                      </div>
                      <span className="text-sm text-gray-500">
                        {format(new Date(task.created_at), 'MMM d, yyyy')}
                      </span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">No recent tasks</p>
              )}
            </div>
          </div>

          {/* Recent Projects */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-xl font-semibold">Recent Projects</h3>
            </div>
            <div className="p-6">
              {dashboard?.recent_projects && dashboard.recent_projects.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {dashboard.recent_projects.map((project) => (
                    <Link
                      key={project.id}
                      href={`/projects/${project.id}`}
                      className="block p-4 border border-gray-200 rounded-lg hover:border-primary hover:shadow-md transition"
                    >
                      <h4 className="font-semibold text-lg mb-2">{project.name}</h4>
                      {project.description && (
                        <p className="text-sm text-gray-600 mb-2">{project.description}</p>
                      )}
                      <span className="text-xs text-gray-500">
                        {format(new Date(project.created_at), 'MMM d, yyyy')}
                      </span>
                    </Link>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No recent projects</p>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

