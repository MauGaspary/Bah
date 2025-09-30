import { createPortal } from 'react-dom'
import { useEffect, useState } from 'react'

function Modal({ children, onClose, onLogout }) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  const portalRoot = document.body
  if (!portalRoot) return null

  return createPortal(
    <div
      className="fixed inset-0 flex items-center justify-center bg-black/50 z-40"
      onClick={onClose} 
    >
      {children}
    </div>,
    portalRoot
  )
}

export default Modal
