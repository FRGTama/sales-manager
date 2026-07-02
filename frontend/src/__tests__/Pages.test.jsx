import { render, screen } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it, vi } from 'vitest'

vi.mock('../api/hooks', () => ({
  useStats: vi.fn(),
  useSales: vi.fn(),
  useCreateSale: () => ({ mutate: vi.fn(), isPending: false, isError: false }),
  useDeleteSale: () => ({ mutate: vi.fn(), isPending: false, isError: false }),
  useAgencies: vi.fn(),
  useCreateAgency: () => ({ mutate: vi.fn(), isPending: false, isError: false }),
  useTrackRecords: vi.fn(),
  useCreateTrackRecord: () => ({ mutate: vi.fn(), isPending: false, isError: false }),
}))

import { useStats, useSales } from '../api/hooks'
import DashboardPage from '../pages/DashboardPage'
import SalesPage from '../pages/SalesPage'

function wrapper({ children }) {
  return (
    <QueryClientProvider client={new QueryClient({ defaultOptions: { queries: { retry: false } } })}>
      <MemoryRouter>{children}</MemoryRouter>
    </QueryClientProvider>
  )
}

describe('DashboardPage', () => {
  it('shows loading state', () => {
    useStats.mockReturnValue({ data: undefined, isLoading: true })
    render(<DashboardPage />, { wrapper })
    expect(screen.getAllByText('...').length).toBeGreaterThanOrEqual(4)
  })

  it('renders stats with zero data', () => {
    useStats.mockReturnValue({
      data: { active_sales_count: 0, total_agencies: 0, total_track_records: 0, track_records_by_status: {} },
      isLoading: false,
    })
    render(<DashboardPage />, { wrapper })
    expect(screen.getAllByText('0')).toHaveLength(4)
    expect(screen.getByText('Active Sales')).toBeInTheDocument()
    expect(screen.getByText('Total Agencies')).toBeInTheDocument()
    expect(screen.getByText('Track Records')).toBeInTheDocument()
  })

  it('renders stats with data', () => {
    useStats.mockReturnValue({
      data: { active_sales_count: 5, total_agencies: 10, total_track_records: 25, track_records_by_status: { new: 10, won: 15 } },
      isLoading: false,
    })
    render(<DashboardPage />, { wrapper })
    expect(screen.getByText('5')).toBeInTheDocument()
    expect(screen.getByText('10')).toBeInTheDocument()
    expect(screen.getAllByText('25')).toHaveLength(2)
  })

  it('shows chart section title', () => {
    useStats.mockReturnValue({
      data: { active_sales_count: 0, total_agencies: 0, total_track_records: 0, track_records_by_status: {} },
      isLoading: false,
    })
    render(<DashboardPage />, { wrapper })
    expect(screen.getByText('Track Records by Status')).toBeInTheDocument()
  })
})

describe('SalesPage', () => {
  it('shows empty state when no sales', () => {
    useSales.mockReturnValue({ data: [], isLoading: false })
    render(<SalesPage />, { wrapper })
    expect(screen.getByText('No sales yet. Add one!')).toBeInTheDocument()
  })

  it('shows loading state', () => {
    useSales.mockReturnValue({ data: undefined, isLoading: true })
    render(<SalesPage />, { wrapper })
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('renders sales list', () => {
    useSales.mockReturnValue({
      data: [{ id: 1, name: 'Alice', phone: '0909123456', email: 'a@b.com', status: 'active', created_at: '2026-01-01' }],
      isLoading: false,
    })
    render(<SalesPage />, { wrapper })
    expect(screen.getByText('Alice')).toBeInTheDocument()
    expect(screen.getByText(/Add Sale/)).toBeInTheDocument()
  })

  it('shows Add Sale button', () => {
    useSales.mockReturnValue({ data: [], isLoading: false })
    render(<SalesPage />, { wrapper })
    expect(screen.getByText('+ Add Sale')).toBeInTheDocument()
  })
})
