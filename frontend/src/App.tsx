import { Navigate, Route, Routes } from 'react-router-dom'

import { useAuth } from './context/AuthContext'
import { DashboardPage } from './pages/DashboardPage'
import { LoginPage } from './pages/LoginPage'
import { ProjectDetailsPage } from './pages/ProjectDetailsPage'
import { ProjectsPage } from './pages/ProjectsPage'
import { RegisterPage } from './pages/RegisterPage'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()

  if (loading) return <div className="loading-state">Loading Darukaa.Earth…</div>
  if (!user) return <Navigate to="/login" replace />
  return <>{children}</>
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/projects"
        element={
          <ProtectedRoute>
            <ProjectsPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/projects/:projectId"
        element={
          <ProtectedRoute>
            <ProjectDetailsPage />
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}
