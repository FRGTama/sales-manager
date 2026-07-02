import { useState } from 'react'

import { useCreateAgency, useSales } from '../api/hooks'

export default function AgencyForm({ onSuccess }) {
  const [name, setName] = useState('')
  const [address, setAddress] = useState('')
  const [area, setArea] = useState('')
  const [saleId, setSaleId] = useState('')
  const { data: sales } = useSales()
  const createAgency = useCreateAgency()

  const handleSubmit = (e) => {
    e.preventDefault()
    createAgency.mutate(
      { name, address, area, sale_id: Number(saleId) },
      { onSuccess: () => { setName(''); setAddress(''); setArea(''); setSaleId(''); onSuccess?.() } },
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
      <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Address" value={address} onChange={(e) => setAddress(e.target.value)} required />
      <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Area" value={area} onChange={(e) => setArea(e.target.value)} required />
      <select className="w-full border rounded-lg px-3 py-2 text-sm" value={saleId} onChange={(e) => setSaleId(e.target.value)} required>
        <option value="">Select Sale...</option>
        {sales?.map((s) => (
          <option key={s.id} value={s.id}>{s.name}</option>
        ))}
      </select>
      <button type="submit" disabled={createAgency.isPending} className="w-full bg-blue-600 text-white rounded-lg py-2 text-sm font-medium hover:bg-blue-700 disabled:opacity-50 cursor-pointer">
        {createAgency.isPending ? 'Saving...' : 'Create Agency'}
      </button>
      {createAgency.isError && <p className="text-red-500 text-xs">{createAgency.error.message}</p>}
    </form>
  )
}
