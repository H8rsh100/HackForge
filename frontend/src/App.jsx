import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Hackathons from './pages/Hackathons'
import Teams from './pages/Teams'
import Analytics from './pages/Analytics'

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/hackathons" element={<Hackathons />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}