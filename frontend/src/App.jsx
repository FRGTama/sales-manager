import { BrowserRouter, Route, Routes } from 'react-router-dom'

import Layout from './components/Layout'
import AgenciesPage from './pages/AgenciesPage'
import DashboardPage from './pages/DashboardPage'
import SalesPage from './pages/SalesPage'
import TrackRecordsPage from './pages/TrackRecordsPage'

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/sales" element={<SalesPage />} />
          <Route path="/agencies" element={<AgenciesPage />} />
          <Route path="/track-records" element={<TrackRecordsPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
