import { useState } from 'react'

import { useCreateSale } from '../api/hooks'

export default function SaleForm({ onSuccess }) {
  const [name, setName] = useState('')
  const [phone, setPhone] = useState('')
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState('active')
  const createSale = useCreateSale()

  const handleSubmit = (e) => {
    e.preventDefault()
    createSale.mutate(
      { name, phone, email, status },
      { onSuccess: () => { setName(''); setPhone(''); setEmail(''); setStatus('active'); onSuccess?.() } },
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
      <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Phone" value={phone} onChange={(e) => setPhone(e.target.value)} required />
      <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <select className="w-full border rounded-lg px-3 py-2 text-sm" value={status} onChange={(e) => setStatus(e.target.value)}>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
      <button type="submit" disabled={createSale.isPending} className="w-full bg-blue-600 text-white rounded-lg py-2 text-sm font-medium hover:bg-blue-700 disabled:opacity-50 cursor-pointer">
        {createSale.isPending ? 'Saving...' : 'Create Sale'}
      </button>
      {createSale.isError && <p className="text-red-500 text-xs">{createSale.error.message}</p>}
    </form>
  )
}
