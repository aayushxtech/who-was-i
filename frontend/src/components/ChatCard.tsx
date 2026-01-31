interface ChatCardProps {
  message: string
  username: string
  timestamp: Date
  isOwnMessage?: boolean
}

function ChatCard({ message, username, timestamp, isOwnMessage = false }: ChatCardProps) {
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    })
  }

  return (
    <div className={`mb-2 ${isOwnMessage ? 'ml-24' : 'mr-24'}`}>
      <div 
        className={`rounded-lg p-2 ${
          isOwnMessage 
            ? 'bg-slate-700/50 border border-slate-600/30' 
            : 'bg-slate-800/50 border border-slate-700/30'
        }`}
      >
        {/* Username at top left */}
        <div className="mb-2">
          <span className={`text-sm font-medium lowercase tracking-wide ${
            isOwnMessage ? 'text-slate-200' : 'text-slate-300'
          }`}>
            {username}
          </span>
        </div>

        {/* Message content */}
        <div className="mb-2">
          <p className="text-slate-100 text-base font-light leading-relaxed whitespace-pre-wrap break-words">
            {message}
          </p>
        </div>

        {/* Timestamp at bottom right */}
        <div className="flex justify-end">
          <span className="text-xs text-slate-500 font-light">
            {formatTime(timestamp)}
          </span>
        </div>
      </div>
    </div>
  )
}

export default ChatCard