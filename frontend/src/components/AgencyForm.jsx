import { useState } from 'react'

import { useCreateAgency, useSales, useUpdateAgency } from '../api/hooks'

const AREAS = [
  'An Giang', 'Bắc Ninh', 'Cà Mau', 'Cao Bằng', 'Cần Thơ', 'Đắk Lắk',
  'Đà Nẵng', 'Điện Biên', 'Đồng Nai', 'Đồng Tháp', 'Gia Lai', 'Hà Nội',
  'Hà Tĩnh', 'Hải Phòng', 'Hồ Chí Minh', 'Huế', 'Hưng Yên', 'Khánh Hòa',
  'Lai Châu', 'Lâm Đồng', 'Lạng Sơn', 'Lào Cai', 'Nghệ An', 'Ninh Bình',
  'Phú Thọ', 'Quảng Ninh', 'Quảng Ngãi', 'Quảng Trị', 'Sơn La', 'Tây Ninh',
  'Thái Nguyên', 'Thanh Hóa', 'Tuyên Quang', 'Vĩnh Long',
]

export default function AgencyForm({ initialData, onSuccess }) {
  const [name, setName] = useState(initialData?.name ?? '')
  const [address, setAddress] = useState(initialData?.address ?? '')
  const [area, setArea] = useState(initialData?.area ?? '')
  const [saleId, setSaleId] = useState(initialData?.sale_id ?? '')
  const { data: sales } = useSales()
  const createAgency = useCreateAgency()
  const updateAgency = useUpdateAgency()
  const isEdit = !!initialData

  const handleSubmit = (e) => {
    e.preventDefault()
    const payload = { name, address, area, sale_id: Number(saleId) }
    const mutation = isEdit ? updateAgency : createAgency
    mutation.mutate(
      isEdit ? { id: initialData.id, ...payload } : payload,
      {
        onSuccess: () => {
          if (!isEdit) { setName(''); setAddress(''); setArea(''); setSaleId('') }
          onSuccess?.()
        },
      },
    )
  }

  const isPending = createAgency.isPending || updateAgency.isPending
  const isError = createAgency.isError || updateAgency.isError
  const error = createAgency.error ?? updateAgency.error

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
      <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Address" value={address} onChange={(e) => setAddress(e.target.value)} required />
      <select className="w-full border rounded-lg px-3 py-2 text-sm" value={area} onChange={(e) => setArea(e.target.value)} required>
        <option value="">Select Area...</option>
        {AREAS.map((a) => (
          <option key={a} value={a}>{a}</option>
        ))}
      </select>
      <select className="w-full border rounded-lg px-3 py-2 text-sm" value={saleId} onChange={(e) => setSaleId(e.target.value)} required>
        <option value="">Select Sale...</option>
        {sales?.map((s) => (
          <option key={s.id} value={s.id}>{s.name}</option>
        ))}
      </select>
      <button type="submit" disabled={isPending} className="w-full bg-blue-600 text-white rounded-lg py-2 text-sm font-medium hover:bg-blue-700 disabled:opacity-50 cursor-pointer">
        {isPending ? 'Saving...' : isEdit ? 'Update Agency' : 'Create Agency'}
      </button>
      {isError && <p className="text-red-500 text-xs">{error.message}</p>}
    </form>
  )
}
