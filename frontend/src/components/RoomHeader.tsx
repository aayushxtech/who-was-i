import { useEffect, useState } from 'react'
import { Link } from '@tanstack/react-router'
import SetDisplayName from './SetDisplayName'

interface RoomHeaderProps {
  roomName: string
}

function RoomHeader({ roomName }: RoomHeaderProps) {
  const [showDisplayNameModal, setShowDisplayNameModal] = useState(false)
  const [currentDisplayName, setCurrentDisplayName] = useState('')

  useEffect(() => {
    // Load display name from session storage on mount
    const savedDisplayName = sessionStorage.getItem('displayName')
    if (savedDisplayName) {
      setCurrentDisplayName(savedDisplayName)
    }
  }, [])

  const handleSetDisplayName = () => {
    setShowDisplayNameModal(true)
  }

  const handleCloseModal = () => {
    setShowDisplayNameModal(false)
  }

  const handleSaveDisplayName = (displayName: string) => {
    setCurrentDisplayName(displayName)
  }

  return (
    <>
      <header className="sticky top-0 z-10 flex items-center justify-between p-3 sm:p-6 border-b border-slate-700/50 bg-slate-800 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <Link
            to="/"
            className="flex items-center justify-center w-8 h-8 rounded-lg bg-slate-700/50 hover:bg-slate-700 transition-colors group"
            aria-label="Go back to home"
          >
            <svg
              className="w-4 h-4 text-slate-400 group-hover:text-slate-200 transition-colors"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <h1 className="text-base sm:text-lg font-semibold text-slate-100 lowercase truncate">
            {roomName}
          </h1>
        </div>
        
        <button
          onClick={handleSetDisplayName}
          className="text-xs sm:text-sm font-light text-slate-400 hover:text-slate-200 lowercase tracking-wide transition-colors whitespace-nowrap"
        >
          {currentDisplayName ? `${currentDisplayName} • change` : 'set display name'}
        </button>
      </header>

      {showDisplayNameModal && (
        <SetDisplayName
          onClose={handleCloseModal}
          onSave={handleSaveDisplayName}
          currentDisplayName={currentDisplayName}
        />
      )}
    </>
  )
}

export default RoomHeader