import { useState } from 'react'

import { useAgencies } from '../api/hooks'
import AgencyForm from '../components/AgencyForm'
import DataTable from '../components/DataTable'
import Modal from '../components/Modal'

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'name', label: 'Name' },
  { key: 'address', label: 'Address' },
  { key: 'area', label: 'Area' },
  { key: 'sale_name', label: 'Sale' },
]

export default function AgenciesPage() {
  const { data, isLoading } = useAgencies()
  const [modalOpen, setModalOpen] = useState(false)

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Agencies</h2>
        <button onClick={() => setModalOpen(true)} className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 cursor-pointer">
          + Add Agency
        </button>
      </div>

      <div className="bg-white border rounded-xl">
        <DataTable columns={columns} data={data} loading={isLoading} emptyMessage="No agencies yet. Add one!" />
      </div>

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="New Agency">
        <AgencyForm onSuccess={() => setModalOpen(false)} />
      </Modal>
    </div>
  )
}
