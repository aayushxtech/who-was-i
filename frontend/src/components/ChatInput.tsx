import { useEffect, useRef, useState } from 'react'
import { SendHorizontal } from 'lucide-react'

interface ChatInputProps {
  onSendMessage: (messageBytes: Uint8Array) => void
  disabled?: boolean
  placeholder?: string
}

function ChatInput({ onSendMessage, disabled = false, placeholder = "say something..." }: ChatInputProps) {
  const [message, setMessage] = useState('')
  const [displayName, setDisplayName] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    // Auto-resize textarea based on content
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [message])

  useEffect(() => {
    // Check for display name on mount and when storage changes
    const checkDisplayName = () => {
      const savedDisplayName = sessionStorage.getItem('displayName')
      setDisplayName(savedDisplayName || '')
    }

    checkDisplayName()

    // Listen for storage changes
    window.addEventListener('storage', checkDisplayName)
    
    // Also check periodically in case sessionStorage was updated in same tab
    const interval = setInterval(checkDisplayName, 1000)

    return () => {
      window.removeEventListener('storage', checkDisplayName)
      clearInterval(interval)
    }
  }, [])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const trimmedMessage = message.trim()
    
    if (!trimmedMessage || disabled || !displayName) {
      return
    }

    // Convert message to bytes
    const encoder = new TextEncoder()
    const messageBytes = encoder.encode(trimmedMessage)
    
    // Send the message
    onSendMessage(messageBytes)
    
    // Clear the input
    setMessage('')
    
    // Keep focus on textarea for continued typing
    if (textareaRef.current) {
      textareaRef.current.focus()
    }
  }

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSubmit(event)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value)
  }

  const canSend = message.trim() && !disabled && displayName

  return (
    <div className="fixed bottom-0 left-0 right-0 border-t border-slate-700/50 p-3 sm:p-4 bg-slate-800 z-20">
      <div className="max-w-4xl mx-auto">
        <form onSubmit={handleSubmit} className="flex gap-2 sm:gap-3 items-end">
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={handleChange}
              onKeyDown={handleKeyDown}
              disabled={disabled || !displayName}
              placeholder={!displayName ? "set a display name first..." : placeholder}
              className="w-full bg-slate-900/40 border border-slate-700/50 rounded-lg px-3 sm:px-4 py-3 text-slate-100 text-sm sm:text-base font-light resize-none focus:outline-none focus:border-slate-600 focus:bg-slate-900/60 transition-all duration-200 placeholder:text-slate-500 disabled:opacity-50 disabled:cursor-not-allowed"
              rows={1}
              maxLength={1000}
              style={{ minHeight: '44px', maxHeight: '100px' }}
            />
          </div>
          
          <button
            type="submit"
            disabled={!canSend}
            className="bg-slate-700 hover:bg-slate-600 active:bg-slate-500 disabled:bg-slate-800 disabled:text-slate-500 border border-slate-600/50 rounded-lg p-3 text-slate-100 transition-all duration-200 focus:outline-none focus:bg-slate-600 touch-manipulation"
            aria-label="Send message"
          >
            <SendHorizontal size={16} className="sm:w-4.5 sm:h-4.5" />
          </button>
        </form>
        
        <div className="mt-2 text-xs text-slate-500 text-center hidden sm:block">
          {!displayName 
            ? "set your display name to start chatting" 
            : "press enter to send • shift + enter for new line"
          }
        </div>
      </div>
    </div>
  )
}

export default ChatInput