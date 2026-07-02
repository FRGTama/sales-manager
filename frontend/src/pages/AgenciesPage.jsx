import { useState } from 'react'

import { useAgencies, useDeleteAgency } from '../api/hooks'
import AgencyForm from '../components/AgencyForm'
import DataTable from '../components/DataTable'
import Modal from '../components/Modal'

export default function AgenciesPage() {
  const { data, isLoading } = useAgencies()
  const deleteAgency = useDeleteAgency()
  const [modalOpen, setModalOpen] = useState(false)
  const [editTarget, setEditTarget] = useState(null)

  const handleDelete = (agency) => {
    if (window.confirm(`Delete agency "${agency.name}"? This will also remove all associated track records.`)) {
      deleteAgency.mutate(agency.id)
    }
  }

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { key: 'address', label: 'Address' },
    { key: 'area', label: 'Area' },
    { key: 'sale_name', label: 'Sale' },
    { key: 'actions', label: 'Actions', render: (row) => (
      <div className="flex gap-2">
        <button onClick={() => setEditTarget(row)} className="text-blue-600 hover:text-blue-800 text-xs font-medium cursor-pointer">Edit</button>
        <button onClick={() => handleDelete(row)} className="text-red-600 hover:text-red-800 text-xs font-medium cursor-pointer">Delete</button>
      </div>
    )},
  ]

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

      <Modal isOpen={!!editTarget} onClose={() => setEditTarget(null)} title="Edit Agency">
        {editTarget && <AgencyForm key={editTarget.id} initialData={editTarget} onSuccess={() => setEditTarget(null)} />}
      </Modal>
    </div>
  )
}
