import { useState } from 'react'

import { useTrackRecords } from '../api/hooks'
import DataTable from '../components/DataTable'
import Modal from '../components/Modal'
import TrackRecordForm from '../components/TrackRecordForm'

const STATUS_STYLES = {
  new: 'bg-blue-100 text-blue-700',
  contacted: 'bg-yellow-100 text-yellow-700',
  potential: 'bg-purple-100 text-purple-700',
  won: 'bg-green-100 text-green-700',
  lost: 'bg-red-100 text-red-700',
}

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'customer_name', label: 'Customer' },
  { key: 'expected_revenue', label: 'Revenue',
    render: (row) => `$${Number(row.expected_revenue).toLocaleString()}` },
  { key: 'status', label: 'Status',
    render: (row) => (
      <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_STYLES[row.status] ?? 'bg-gray-100 text-gray-500'}`}>
        {row.status}
      </span>
    ),
  },
  { key: 'agency_name', label: 'Agency' },
  { key: 'notes', label: 'Notes',
    render: (row) => row.notes || <span className="text-gray-300">&mdash;</span> },
]

export default function TrackRecordsPage() {
  const { data, isLoading } = useTrackRecords()
  const [modalOpen, setModalOpen] = useState(false)

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Track Records</h2>
        <button onClick={() => setModalOpen(true)} className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 cursor-pointer">
          + Add Track Record
        </button>
      </div>

      <div className="bg-white border rounded-xl">
        <DataTable columns={columns} data={data} loading={isLoading} emptyMessage="No track records yet. Add one!" />
      </div>

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="New Track Record">
        <TrackRecordForm onSuccess={() => setModalOpen(false)} />
      </Modal>
    </div>
  )
}
