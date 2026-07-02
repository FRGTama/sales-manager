import { useState } from 'react'

import { useCreateSale, useUpdateSale } from '../api/hooks'

export default function SaleForm({ initialData, onSuccess }) {
  const [name, setName] = useState(initialData?.name ?? '')
  const [phone, setPhone] = useState(initialData?.phone ?? '')
  const [phoneError, setPhoneError] = useState('')
  const [email, setEmail] = useState(initialData?.email ?? '')
  const [status, setStatus] = useState(initialData?.status ?? 'active')
  const createSale = useCreateSale()
  const updateSale = useUpdateSale()
  const isEdit = !!initialData

  const validatePhone = (value) => {
    setPhone(value)
    if (value && !/^0\d{9}$/.test(value)) {
      setPhoneError('Must be 10 digits starting with 0')
    } else {
      setPhoneError('')
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (phoneError) return
    const payload = { name, phone, email, status }
    const mutation = isEdit ? updateSale : createSale
    mutation.mutate(
      isEdit ? { id: initialData.id, ...payload } : payload,
      {
        onSuccess: () => {
          if (!isEdit) { setName(''); setPhone(''); setPhoneError(''); setEmail(''); setStatus('active') }
          onSuccess?.()
        },
      },
    )
  }

  const isPending = createSale.isPending || updateSale.isPending
  const isError = createSale.isError || updateSale.isError
  const error = createSale.error ?? updateSale.error

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
      <div>
        <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Phone" type="tel" inputMode="numeric" maxLength={10} value={phone} onChange={(e) => validatePhone(e.target.value)} required />
        {phoneError && <p className="text-red-500 text-xs mt-1">{phoneError}</p>}
      </div>
      <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <select className="w-full border rounded-lg px-3 py-2 text-sm" value={status} onChange={(e) => setStatus(e.target.value)}>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
      <button type="submit" disabled={isPending} className="w-full bg-blue-600 text-white rounded-lg py-2 text-sm font-medium hover:bg-blue-700 disabled:opacity-50 cursor-pointer">
        {isPending ? 'Saving...' : isEdit ? 'Update Sale' : 'Create Sale'}
      </button>
      {isError && <p className="text-red-500 text-xs">{error.message}</p>}
    </form>
  )
}
