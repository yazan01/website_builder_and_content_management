import { cn } from '../../utils/cn'
import { X } from 'lucide-react'

interface ModalProps {
  open: boolean
  onClose: () => void
  title?: string
  children: React.ReactNode
  className?: string
}

export function Modal({ open, onClose, title, children, className }: ModalProps) {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div className={cn('relative bg-white rounded-xl shadow-2xl w-full max-w-md p-6', className)}>
        <div className="flex items-center justify-between mb-4">
          {title && <h2 className="text-lg font-semibold text-slate-900">{title}</h2>}
          <button onClick={onClose} className="ml-auto p-1 rounded hover:bg-slate-100 text-slate-500">
            <X size={18} />
          </button>
        </div>
        {children}
      </div>
    </div>
  )
}
