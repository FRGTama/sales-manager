import { NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Dashboard', icon: '📊' },
  { to: '/sales', label: 'Sales', icon: '👤' },
  { to: '/agencies', label: 'Agencies', icon: '🏢' },
  { to: '/track-records', label: 'Track Records', icon: '📝' },
]

export default function Layout({ children }) {
  return (
    <div className="flex h-screen bg-gray-50">
      <nav className="w-64 bg-white border-r border-gray-200 p-4 flex flex-col gap-2">
        <h1 className="text-lg font-bold text-gray-800 mb-4 px-3">Sales Manager</h1>
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            end={l.to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition ${
                isActive
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`
            }
          >
            <span>{l.icon}</span>
            {l.label}
          </NavLink>
        ))}
      </nav>
      <main className="flex-1 overflow-auto p-6">{children}</main>
    </div>
  )
}
