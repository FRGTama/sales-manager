import { useState } from 'react'

import { useAgencies, useCreateTrackRecord } from '../api/hooks'

const STATUS_OPTIONS = ['new', 'contacted', 'potential', 'won', 'lost']

export default function TrackRecordForm({ onSuccess }) {
  const [customerName, setCustomerName] = useState('')
  const [expectedRevenue, setExpectedRevenue] = useState('')
  const [status, setStatus] = useState('new')
  const [notes, setNotes] = useState('')
  const [agencyId, setAgencyId] = useState('')
  const { data: agencies } = useAgencies()
  const createRecord = useCreateTrackRecord()

  const handleSubmit = (e) => {
    e.preventDefault()
    createRecord.mutate(
      {
        customer_name: customerName,
        expected_revenue: Number(expectedRevenue),
        status,
        notes: notes || null,
        agency_id: Number(agencyId),
      },
      {
        onSuccess: () => {
          setCustomerName('')
          setExpectedRevenue('')
          setStatus('new')
          setNotes('')
          setAgencyId('')
          onSuccess?.()
        },
      },
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Customer Name" value={customerName} onChange={(e) => setCustomerName(e.target.value)} required />
      <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Expected Revenue" type="number" min="0" step="0.01" value={expectedRevenue} onChange={(e) => setExpectedRevenue(e.target.value)} required />
      <select className="w-full border rounded-lg px-3 py-2 text-sm" value={status} onChange={(e) => setStatus(e.target.value)}>
        {STATUS_OPTIONS.map((s) => (
          <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
        ))}
      </select>
      <textarea className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Notes (optional)" value={notes} onChange={(e) => setNotes(e.target.value)} rows={2} />
      <select className="w-full border rounded-lg px-3 py-2 text-sm" value={agencyId} onChange={(e) => setAgencyId(e.target.value)} required>
        <option value="">Select Agency...</option>
        {agencies?.map((a) => (
          <option key={a.id} value={a.id}>{a.name}</option>
        ))}
      </select>
      <button type="submit" disabled={createRecord.isPending} className="w-full bg-blue-600 text-white rounded-lg py-2 text-sm font-medium hover:bg-blue-700 disabled:opacity-50 cursor-pointer">
        {createRecord.isPending ? 'Saving...' : 'Create Track Record'}
      </button>
      {createRecord.isError && <p className="text-red-500 text-xs">{createRecord.error.message}</p>}
    </form>
  )
}
