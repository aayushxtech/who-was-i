import { createFileRoute } from '@tanstack/react-router'
import { useEffect, useRef, useState } from 'react'
import RoomHeader from '../../components/RoomHeader'
import ChatCard from '../../components/ChatCard'
import ChatInput from '../../components/ChatInput'

export const Route = createFileRoute('/room/$roomId')({
  component: RoomPage,
})

interface Message {
  id: string
  message: string
  username: string
  timestamp: Date
  isOwnMessage: boolean
}

function RoomPage() {
  const { roomId } = Route.useParams()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [messages, setMessages] = useState<Array<Message>>([
    {
      id: '1',
      message: 'Hello everyone! This is a test message to see how the chat looks.',
      username: 'alice',
      timestamp: new Date(Date.now() - 10 * 60 * 1000), // 10 minutes ago
      isOwnMessage: false,
    },
    {
      id: '2',
      message: 'Hey there! Nice to meet you all.',
      username: 'you',
      timestamp: new Date(Date.now() - 5 * 60 * 1000), // 5 minutes ago
      isOwnMessage: true,
    },
    {
      id: '3',
      message: 'This is another message from someone else in the room.',
      username: 'bob',
      timestamp: new Date(Date.now() - 2 * 60 * 1000), // 2 minutes ago
      isOwnMessage: false,
    },
  ])

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = (messageBytes: Uint8Array) => {
    // Decode bytes back to string for now
    const decoder = new TextDecoder()
    const messageText = decoder.decode(messageBytes)
    
    // Get current display name from session storage
    const displayName = sessionStorage.getItem('displayName') || 'anonymous'
    
    // Create new message
    const newMessage: Message = {
      id: Date.now().toString(),
      message: messageText,
      username: displayName,
      timestamp: new Date(),
      isOwnMessage: true,
    }
    
    // Add to messages
    setMessages(prev => [...prev, newMessage])
    
    // Here you would typically send the messageBytes to your backend/WebSocket
    console.log('Sending message bytes:', messageBytes)
  }

  return (
    <div className="min-h-screen bg-slate-800 flex flex-col">
      <RoomHeader roomName={roomId} />
      
      <main className="flex-1 min-h-0">
        <div className="h-full overflow-y-auto">
          <div className="max-w-4xl mx-auto px-3 sm:px-4 py-3 sm:py-4 pb-6">
            {messages.map(msg => (
              <ChatCard
                key={msg.id}
                message={msg.message}
                username={msg.username}
                timestamp={msg.timestamp}
                isOwnMessage={msg.isOwnMessage}
              />
            ))}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </main>
      
      <div className="shrink-0">
        <ChatInput
          onSendMessage={handleSendMessage}
          placeholder="share a thought..."
        />
      </div>
    </div>
  )
}
