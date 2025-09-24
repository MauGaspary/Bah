import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import { AuthProvider } from './contexts/AuthContext'
import DashboardPage from './pages/DashboardPage'
import HomePage from './pages/HomePage'
import LoginAdminPage from './pages/LoginAdminPage'
import FormIniciativa from './pages/formIniciativa'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/admin" element={<LoginAdminPage />} />
          <Route path="/CriarIniciativa" element={<FormIniciativa />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
