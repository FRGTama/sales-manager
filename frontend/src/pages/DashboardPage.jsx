import { useStats } from '../api/hooks'
import StatCard from '../components/StatCard'
import StatusChart from '../components/StatusChart'

export default function DashboardPage() {
  const { data, isLoading } = useStats()

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Active Sales" value={isLoading ? '...' : data?.active_sales_count ?? 0} color="blue" />
        <StatCard label="Total Agencies" value={isLoading ? '...' : data?.total_agencies ?? 0} color="green" />
        <StatCard label="Track Records" value={isLoading ? '...' : data?.total_track_records ?? 0} color="purple" />
        <StatCard
          label="Status Breakdown"
          value={isLoading ? '...' : Object.values(data?.track_records_by_status ?? {}).reduce((a, b) => a + b, 0)}
          color="orange"
        />
      </div>

      <div className="bg-white border rounded-xl p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Track Records by Status</h3>
        {isLoading ? (
          <p className="text-gray-400 text-sm">Loading...</p>
        ) : (
          <StatusChart data={data?.track_records_by_status} />
        )}
      </div>
    </div>
  )
}
