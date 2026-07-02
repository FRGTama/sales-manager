import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import DataTable from '../components/DataTable'

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'name', label: 'Name' },
]

describe('DataTable', () => {
  it('shows loading state', () => {
    render(<DataTable columns={columns} data={[]} loading={true} />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('shows empty message when no data', () => {
    render(<DataTable columns={columns} data={[]} loading={false} />)
    expect(screen.getByText('No data')).toBeInTheDocument()
  })

  it('shows custom empty message', () => {
    render(<DataTable columns={columns} data={[]} loading={false} emptyMessage="Nothing here" />)
    expect(screen.getByText('Nothing here')).toBeInTheDocument()
  })

  it('renders table headers', () => {
    render(<DataTable columns={columns} data={[{ id: 1, name: 'Alice' }]} loading={false} />)
    expect(screen.getByText('ID')).toBeInTheDocument()
    expect(screen.getByText('Name')).toBeInTheDocument()
  })

  it('renders data rows', () => {
    render(<DataTable columns={columns} data={[{ id: 1, name: 'Alice' }]} loading={false} />)
    expect(screen.getByText('Alice')).toBeInTheDocument()
  })

  it('renders multiple rows', () => {
    const data = [
      { id: 1, name: 'Alice' },
      { id: 2, name: 'Bob' },
    ]
    render(<DataTable columns={columns} data={data} loading={false} />)
    expect(screen.getByText('Alice')).toBeInTheDocument()
    expect(screen.getByText('Bob')).toBeInTheDocument()
  })

  it('uses custom render function', () => {
    const cols = [
      { key: 'id', label: 'ID' },
      { key: 'name', label: 'Upper', render: (row) => row.name.toUpperCase() },
    ]
    render(<DataTable columns={cols} data={[{ id: 1, name: 'Alice' }]} loading={false} />)
    expect(screen.getByText('ALICE')).toBeInTheDocument()
  })

  it('handles null data gracefully', () => {
    render(<DataTable columns={columns} data={null} loading={false} />)
    expect(screen.getByText('No data')).toBeInTheDocument()
  })

  it('handles undefined data gracefully', () => {
    render(<DataTable columns={columns} data={undefined} loading={false} />)
    expect(screen.getByText('No data')).toBeInTheDocument()
  })
})
