import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'

import Layout from '../components/Layout'

describe('Layout', () => {
  it('renders app title', () => {
    render(
      <MemoryRouter>
        <Layout><div>Content</div></Layout>
      </MemoryRouter>,
    )
    expect(screen.getByText('Sales Manager')).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    render(
      <MemoryRouter>
        <Layout><div>Content</div></Layout>
      </MemoryRouter>,
    )
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Sales')).toBeInTheDocument()
    expect(screen.getByText('Agencies')).toBeInTheDocument()
    expect(screen.getByText('Track Records')).toBeInTheDocument()
  })

  it('renders children content', () => {
    render(
      <MemoryRouter>
        <Layout><div>Page Content Here</div></Layout>
      </MemoryRouter>,
    )
    expect(screen.getByText('Page Content Here')).toBeInTheDocument()
  })
})
