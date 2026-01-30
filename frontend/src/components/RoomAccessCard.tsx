import { useState } from 'react'

type Mode = 'create' | 'join'

interface RoomAccessCardProps {
  onClose: () => void
  onCreateRoom: (roomName: string, password: string) => void
  onJoinRoom: (roomCode: string, password: string) => void
}

function RoomAccessCard({ onClose, onCreateRoom, onJoinRoom }: RoomAccessCardProps) {
  const [mode, setMode] = useState<Mode>('create')
  const [roomName, setRoomName] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [roomCode, setRoomCode] = useState('')
  const [accessPassword, setAccessPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    if (mode === 'create') {
      if (!roomName.trim() || !newPassword.trim()) {
        setError('room name and password required')
        return
      }
      onCreateRoom(roomName.trim(), newPassword.trim())
    } else {
      if (!roomCode.trim() || !accessPassword.trim()) {
        setError('room code and password required')
        return
      }
      onJoinRoom(roomCode.trim(), accessPassword.trim())
    }
  }

  const handleModeSwitch = (newMode: Mode) => {
    setMode(newMode)
    setError('')
    // Clear form fields when switching modes
    setRoomName('')
    setNewPassword('')
    setRoomCode('')
    setAccessPassword('')
  }

  return (
    <div 
      className="fixed inset-0 bg-slate-900/70 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div 
        className="bg-slate-800 border border-slate-700 rounded-xl p-12 w-full max-w-md shadow-xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Mode Selector */}
        <div className="mb-12">
          <div className="flex bg-slate-900/50 rounded-lg p-1 border border-slate-700/30">
            <button
              onClick={() => handleModeSwitch('create')}
              className={`flex-1 py-3 text-base font-light lowercase tracking-wide rounded-md transition-all duration-150 ${
                mode === 'create' 
                  ? 'bg-slate-700/80 text-slate-100 shadow-sm' 
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              create a room
            </button>
            <button
              onClick={() => handleModeSwitch('join')}
              className={`flex-1 py-3 text-base font-light lowercase tracking-wide rounded-md transition-all duration-150 ${
                mode === 'join' 
                  ? 'bg-slate-700/80 text-slate-100 shadow-sm' 
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              join a room
            </button>
          </div>
        </div>

        {/* Form Content */}
        <form onSubmit={handleSubmit} className="space-y-8">
          {mode === 'create' ? (
            <>
              <div className="space-y-3">
                <label className="block text-sm font-light text-slate-400 lowercase tracking-wide">
                  room name
                </label>
                <input
                  type="text"
                  value={roomName}
                  onChange={(e) => setRoomName(e.target.value)}
                  className="w-full bg-slate-900/40 border border-slate-600/50 rounded-lg px-5 py-4 text-slate-100 text-base font-light focus:outline-none focus:border-slate-500 focus:bg-slate-900/60 transition-colors placeholder:text-slate-500"
                  placeholder="a quiet place"
                  autoFocus
                />
              </div>
              <div className="space-y-3">
                <label className="block text-sm font-light text-slate-400 lowercase tracking-wide">
                  password
                </label>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="w-full bg-slate-900/40 border border-slate-600/50 rounded-lg px-5 py-4 text-slate-100 text-base font-light focus:outline-none focus:border-slate-500 focus:bg-slate-900/60 transition-colors placeholder:text-slate-500"
                  placeholder="something you'll remember"
                />
              </div>
            </>
          ) : (
            <>
              <div className="space-y-3">
                <label className="block text-sm font-light text-slate-400 lowercase tracking-wide">
                  room code
                </label>
                <input
                  type="text"
                  value={roomCode}
                  onChange={(e) => setRoomCode(e.target.value)}
                  className="w-full bg-slate-900/40 border border-slate-600/50 rounded-lg px-5 py-4 text-slate-100 text-base font-light focus:outline-none focus:border-slate-500 focus:bg-slate-900/60 transition-colors placeholder:text-slate-500"
                  placeholder="where you're headed"
                  autoFocus
                />
              </div>
              <div className="space-y-3">
                <label className="block text-sm font-light text-slate-400 lowercase tracking-wide">
                  password
                </label>
                <input
                  type="password"
                  value={accessPassword}
                  onChange={(e) => setAccessPassword(e.target.value)}
                  className="w-full bg-slate-900/40 border border-slate-600/50 rounded-lg px-5 py-4 text-slate-100 text-base font-light focus:outline-none focus:border-slate-500 focus:bg-slate-900/60 transition-colors placeholder:text-slate-500"
                  placeholder="the way in"
                />
              </div>
            </>
          )}

          <button
            type="submit"
            className="w-full bg-slate-700 hover:bg-slate-600 border border-slate-600/50 rounded-lg px-5 py-4 text-slate-100 text-base font-light lowercase tracking-wide transition-colors focus:outline-none focus:bg-slate-600"
          >
            {mode}
          </button>

          {error && (
            <p className="text-sm font-light text-slate-400 text-center lowercase tracking-wide">
              {error}
            </p>
          )}
        </form>
      </div>
    </div>
  )
}

export default RoomAccessCard
