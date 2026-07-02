import { useState } from 'react'

import { useSales } from '../api/hooks'
import DataTable from '../components/DataTable'
import Modal from '../components/Modal'
import SaleForm from '../components/SaleForm'

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'name', label: 'Name' },
  { key: 'phone', label: 'Phone' },
  { key: 'email', label: 'Email' },
  { key: 'status', label: 'Status', render: (row) => (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${
      row.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'
    }`}>
      {row.status}
    </span>
  )},
]

export default function SalesPage() {
  const { data, isLoading } = useSales()
  const [modalOpen, setModalOpen] = useState(false)

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Sales</h2>
        <button onClick={() => setModalOpen(true)} className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 cursor-pointer">
          + Add Sale
        </button>
      </div>

      <div className="bg-white border rounded-xl">
        <DataTable columns={columns} data={data} loading={isLoading} emptyMessage="No sales yet. Add one!" />
      </div>

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="New Sale">
        <SaleForm onSuccess={() => setModalOpen(false)} />
      </Modal>
    </div>
  )
}
