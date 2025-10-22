import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import { AuthProvider } from './contexts/AuthContext'
import AdminIniciativas from './pages/AdminIniciativas'
import AdminUsuarios from './pages/AdminUsers'
import DashboardPage from './pages/DashboardPage'
import FormIniciativa from './pages/formIniciativa'
import HomePage from './pages/HomePage'
import IniciativaPage from './pages/IniciativaPage'
import LoginAdminPage from './pages/LoginAdminPage'
import ResultsPage from './pages/ResultsPage'

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/iniciativa/:id" element={<IniciativaPage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="/admin" element={<LoginAdminPage />} />
          <Route path="/admin/criarIniciativa" element={<FormIniciativa />} />
          <Route path="/admin/usuarios" element={<AdminUsuarios />} />
          <Route path="/admin/iniciativas" element={<AdminIniciativas />} />
        </Routes>
      </AuthProvider>
    </Router>
  )
}

export default App
