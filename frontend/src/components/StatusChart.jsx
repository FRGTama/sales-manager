import { Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'

const STATUS_COLORS = {
  new: '#3b82f6',
  contacted: '#f59e0b',
  potential: '#8b5cf6',
  won: '#22c55e',
  lost: '#ef4444',
}

export default function StatusChart({ data }) {
  const chartData = Object.entries(data ?? {}).map(([name, value]) => ({
    name,
    value,
    fill: STATUS_COLORS[name] ?? '#9ca3af',
  }))

  if (chartData.length === 0) {
    return <p className="text-gray-400 text-sm">No data</p>
  }

  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={80}
            label={({ name, value }) => `${name}: ${value}`}
          />
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
