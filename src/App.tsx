import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import { AuthProvider } from './contexts/AuthContext'
import AdminIniciativas from './pages/AdminIniciativas'
import AdminUsuarios from './pages/AdminUsers'
import DashboardPage from './pages/DashboardPage'
import HomePage from './pages/HomePage'
import LoginAdminPage from './pages/LoginAdminPage'
import FormIniciativa from './pages/formIniciativa'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Rotas públicas */}
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />

          {/* Rotas administrativas - o AuthProvider cuida da proteção */}
          <Route path="/admin" element={<LoginAdminPage />} />
          <Route path="/admin/criarIniciativa" element={<FormIniciativa />} />
          <Route path="/admin/usuarios" element={<AdminUsuarios />} />
          <Route path="/admin/iniciativas" element={<AdminIniciativas />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
