import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import { AuthProvider } from './contexts/AuthContext'
import AdminIniciativas from './pages/AdminIniciativas'
import AdminUsuarios from './pages/AdminUsers'
import FormIniciativa from './pages/formIniciativa'
import FormUsuario from './pages/formUsuario'
import HomePage from './pages/HomePage'
import IniciativaPage from './pages/IniciativaPage'
import LoginAdminPage from './pages/LoginAdminPage'
import ResultsPage from './pages/ResultsPage'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/iniciativa/:id" element={<IniciativaPage />} />
            <Route path="/results" element={<ResultsPage />} />

            <Route path="/admin" element={<LoginAdminPage />} />
            <Route path="/admin/criarIniciativa" element={<FormIniciativa />} />
            <Route
              path="/admin/iniciativas/:id/editar"
              element={<FormIniciativa />}
            />
            <Route
              path="/admin/usuarios/criarUsuario"
              element={<FormUsuario />}
            />
            <Route path="/admin/usuarios" element={<AdminUsuarios />} />
            <Route path="/admin/iniciativas" element={<AdminIniciativas />} />
          </Routes>
        </AuthProvider>
      </Router>
    </QueryClientProvider>
  )
}

export default App
