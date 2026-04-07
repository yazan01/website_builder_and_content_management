import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import SitePage from './pages/SitePage'
import BuilderPage from './pages/BuilderPage'
import MediaPage from './pages/MediaPage'
import TemplatesPage from './pages/TemplatesPage'
import PreviewPage from './pages/PreviewPage'
import LayoutEditorPage from './pages/LayoutEditorPage'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const token = useAuthStore((s) => s.token)
  return token ? <>{children}</> : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<PrivateRoute><DashboardPage /></PrivateRoute>} />
        <Route path="/sites/:siteId" element={<PrivateRoute><SitePage /></PrivateRoute>} />
        <Route path="/sites/:siteId/media" element={<PrivateRoute><MediaPage /></PrivateRoute>} />
        <Route path="/sites/:siteId/builder/:pageId" element={<PrivateRoute><BuilderPage /></PrivateRoute>} />
        <Route path="/sites/:siteId/templates/:pageId" element={<PrivateRoute><TemplatesPage /></PrivateRoute>} />
        <Route path="/sites/:siteId/preview/:pageId" element={<PrivateRoute><PreviewPage /></PrivateRoute>} />
        <Route path="/sites/:siteId/layout" element={<PrivateRoute><LayoutEditorPage /></PrivateRoute>} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
