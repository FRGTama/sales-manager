import { render, screen, fireEvent } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import Modal from '../components/Modal'

describe('Modal', () => {
  it('does not render when closed', () => {
    const { container } = render(
      <Modal isOpen={false} onClose={vi.fn()} title="Test">
        <div>Content</div>
      </Modal>,
    )
    expect(container.innerHTML).toBe('')
  })

  it('renders title and content when open', () => {
    render(
      <Modal isOpen={true} onClose={vi.fn()} title="Test Title">
        <div>Modal Content</div>
      </Modal>,
    )
    expect(screen.getByText('Test Title')).toBeInTheDocument()
    expect(screen.getByText('Modal Content')).toBeInTheDocument()
  })

  it('calls onClose when close button clicked', () => {
    const onClose = vi.fn()
    render(
      <Modal isOpen={true} onClose={onClose} title="Test">
        <div>Content</div>
      </Modal>,
    )
    fireEvent.click(screen.getByText('\u00D7'))
    expect(onClose).toHaveBeenCalledTimes(1)
  })
})
