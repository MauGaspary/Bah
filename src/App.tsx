import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

//import Header from './components/ui/Header/Header'
import DashboardPage from './pages/DashboardPage'
import HomePage from './pages/HomePage'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </Router>
  )
}

export default App
