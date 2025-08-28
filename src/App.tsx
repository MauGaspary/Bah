import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'

import HomePage from './pages/HomePage'
import DashboardPage from './pages/DashboardPage'
import LoginAdminPage from './pages/LoginAdminPage'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/admin" element={<LoginAdminPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
