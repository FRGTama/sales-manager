import { useState } from 'react'

import { useAgencies, useCreateTrackRecord, useUpdateTrackRecord } from '../api/hooks'

const STATUS_OPTIONS = ['new', 'contacted', 'potential', 'won', 'lost']

export default function TrackRecordForm({ initialData, onSuccess }) {
  const [customerName, setCustomerName] = useState(initialData?.customer_name ?? '')
  const [expectedRevenue, setExpectedRevenue] = useState(initialData?.expected_revenue?.toString() ?? '')
  const [status, setStatus] = useState(initialData?.status ?? 'new')
  const [notes, setNotes] = useState(initialData?.notes ?? '')
  const [agencyId, setAgencyId] = useState(initialData?.agency_id ?? '')
  const { data: agencies } = useAgencies()
  const createRecord = useCreateTrackRecord()
  const updateRecord = useUpdateTrackRecord()
  const isEdit = !!initialData

  const handleSubmit = (e) => {
    e.preventDefault()
    const payload = {
      customer_name: customerName,
      expected_revenue: Number(expectedRevenue),
      status,
      notes: notes || null,
      agency_id: Number(agencyId),
    }
    const mutation = isEdit ? updateRecord : createRecord
    mutation.mutate(
      isEdit ? { id: initialData.id, ...payload } : payload,
      {
        onSuccess: () => {
          if (!isEdit) { setCustomerName(''); setExpectedRevenue(''); setStatus('new'); setNotes(''); setAgencyId('') }
          onSuccess?.()
        },
      },
    )
  }

  const isPending = createRecord.isPending || updateRecord.isPending
  const isError = createRecord.isError || updateRecord.isError
  const error = createRecord.error ?? updateRecord.error

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
      <button type="submit" disabled={isPending} className="w-full bg-blue-600 text-white rounded-lg py-2 text-sm font-medium hover:bg-blue-700 disabled:opacity-50 cursor-pointer">
        {isPending ? 'Saving...' : isEdit ? 'Update Track Record' : 'Create Track Record'}
      </button>
      {isError && <p className="text-red-500 text-xs">{error.message}</p>}
    </form>
  )
}
