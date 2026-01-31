import { useEffect, useState} from 'react'

interface SetDisplayNameProps {
  onClose: () => void
  onSave: (displayName: string) => void
  currentDisplayName?: string
}

function SetDisplayName({ onClose, onSave, currentDisplayName = '' }: SetDisplayNameProps) {
  const [displayName, setDisplayName] = useState(currentDisplayName)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    // Subtle entrance animation
    const timer = setTimeout(() => setIsVisible(true), 50)
    return () => clearTimeout(timer)
  }, [])

  useEffect(() => {
    // Handle escape key
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [onClose])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const trimmedName = displayName.trim()
    
    if (!trimmedName) {
      return
    }

    // Save to session storage
    sessionStorage.setItem('displayName', trimmedName)
    
    // Call parent callback
    onSave(trimmedName)
    onClose()
  }

  return (
    <div
      className={`fixed inset-0 bg-slate-900/70 backdrop-blur-sm flex items-center justify-center p-4 transition-opacity duration-300 ${
        isVisible ? 'opacity-100' : 'opacity-0'
      }`}
      onClick={onClose}
    >
      <div
        className={`bg-slate-800 border border-slate-700/50 rounded-xl p-10 w-full max-w-sm shadow-2xl transform transition-all duration-300 ${
          isVisible ? 'scale-100 translate-y-0' : 'scale-95 translate-y-4'
        }`}
        onClick={(e) => e.stopPropagation()}
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="text-center mb-8">
            <h2 className="text-lg font-light text-slate-100 lowercase tracking-wide">
              how should others see you?
            </h2>
          </div>

          <div className="space-y-3">
            <label className="block text-sm font-light text-slate-400 lowercase tracking-wide">
              display name
            </label>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              className="w-full bg-slate-900/50 border border-slate-700/50 rounded-lg px-5 py-4 text-slate-100 text-base font-light focus:outline-none focus:border-slate-600 focus:bg-slate-900/70 transition-all duration-200 placeholder:text-slate-500"
              placeholder="someone quiet"
              autoFocus
              maxLength={30}
            />
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-transparent border border-slate-600/50 rounded-lg px-4 py-3 text-slate-400 text-sm font-light lowercase transition-all duration-200 hover:text-slate-200 hover:border-slate-500"
            >
              cancel
            </button>
            <button
              type="submit"
              disabled={!displayName.trim()}
              className="flex-1 bg-slate-700 hover:bg-slate-600 disabled:bg-slate-800 disabled:text-slate-500 border border-slate-600/50 rounded-lg px-4 py-3 text-slate-100 text-sm font-light lowercase transition-all duration-200 focus:outline-none focus:bg-slate-600"
            >
              save
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default SetDisplayName