import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import StatCard from '../components/StatCard'

describe('StatCard', () => {
  it('renders label and value', () => {
    render(<StatCard label="Active Sales" value={42} />)
    expect(screen.getByText('Active Sales')).toBeInTheDocument()
    expect(screen.getByText('42')).toBeInTheDocument()
  })

  it('renders zero value', () => {
    render(<StatCard label="Count" value={0} />)
    expect(screen.getByText('0')).toBeInTheDocument()
  })

  it('renders string value', () => {
    render(<StatCard label="Status" value="N/A" />)
    expect(screen.getByText('N/A')).toBeInTheDocument()
  })
})
