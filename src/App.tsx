import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

//import Header from './components/ui/Header/Header'
import { AuthProvider } from './contexts/AuthContext'
import AdminIniciativas from './pages/AdminIniciativas'
import AdminUsuarios from './pages/AdminUsers'
import DashboardPage from './pages/DashboardPage'
import HomePage from './pages/HomePage'
import LoginAdminPage from './pages/LoginAdminPage'



function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/admin" element={<LoginAdminPage />} />
          <Route path="/admin/usuarios" element={<AdminUsuarios />} />
          <Route path="/admin/iniciativas" element={<AdminIniciativas />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
