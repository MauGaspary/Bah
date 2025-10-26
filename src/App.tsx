import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import { AuthProvider } from './contexts/AuthContext'
import AdminIniciativas from './pages/AdminIniciativas'
import AdminUsuarios from './pages/AdminUsers'
import DashboardPage from './pages/DashboardPage'
import HomePage from './pages/HomePage'
import LoginAdminPage from './pages/LoginAdminPage'
import FormIniciativa from './pages/formIniciativa'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/dashboard" element={<DashboardPage />} />

            <Route path="/admin" element={<LoginAdminPage />} />
            <Route path="/admin/criarIniciativa" element={<FormIniciativa />} />
            <Route path="/admin/usuarios" element={<AdminUsuarios />} />
            <Route path="/admin/iniciativas" element={<AdminIniciativas />} />
          </Routes>
        </AuthProvider>
      </Router>
    </QueryClientProvider>
  )
}

export default App
