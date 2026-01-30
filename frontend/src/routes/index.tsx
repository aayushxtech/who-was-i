import { useEffect, useState } from 'react'
import { createFileRoute } from '@tanstack/react-router'
import RoomAccessCard from '../components/RoomAccessCard'

export const Route = createFileRoute('/')({
  component: Landing,
})

function Landing() {
  const [visible, setVisible] = useState(false)
  const [ctaVisible, setCtaVisible] = useState(false)
  const [showRoomModal, setShowRoomModal] = useState(false)

  useEffect(() => {
    const fadeIn = setTimeout(() => setVisible(true), 50)
    const ctaDelay = setTimeout(() => setCtaVisible(true), 600)
    return () => {
      clearTimeout(fadeIn)
      clearTimeout(ctaDelay)
    }
  }, [])

  const handleCreateRoom = (roomName: string, password: string) => {
    // Handle room creation logic here
    console.log('Creating room:', roomName, password)
    setShowRoomModal(false)
  }

  const handleJoinRoom = (roomCode: string, password: string) => {
    // Handle room joining logic here
    console.log('Joining room:', roomCode, password)
    setShowRoomModal(false)
  }

  const handleCloseModal = () => {
    setShowRoomModal(false)
  }

  return (
    <>
      <main className="min-h-screen flex items-center justify-center bg-slate-800 relative overflow-hidden">
        {/* Subtle vignette overlay */}
        <div 
          className="absolute inset-0 pointer-events-none"
          style={{
            background: 'radial-gradient(ellipse at center, transparent 0%, rgba(15, 23, 42, 0.15) 100%)'
          }}
        />
        
        {/* Ultra-light grain texture */}
        <div 
          className="absolute inset-0 pointer-events-none opacity-[0.02]"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='1' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
          }}
        />

        <div 
          className={`text-center max-w-md px-6 text-slate-100 transition-opacity duration-1000 ${
            visible ? 'opacity-100' : 'opacity-0'
          }`}
        >
          <h1 className="text-xl font-light tracking-[0.25em] lowercase mb-6 leading-loose text-center" style={{ fontFamily: 'Playfair Display, serif' }}>
            who was i
          </h1>
          

          <p className="text-base font-light opacity-60 leading-relaxed text-center">
            only the words knew
          </p>

          <p className="text-base font-light opacity-60 mb-4 leading-relaxed text-center">
            untill they faded
          </p>

          <p className="text-lg font-medium opacity-40 mb-16 leading-relaxed text-center">
            words that dissolve
          </p>

          <button
            onClick={() => setShowRoomModal(true)}
            className={`text-base font-light lowercase tracking-widest border border-slate-100/20 px-8 py-3 hover:border-slate-100/30 transition-all duration-500 ${
              ctaVisible ? 'opacity-100' : 'opacity-0'
            }`}
            aria-label="enter"
          >
            step inside
          </button>
        </div>
      </main>

      {showRoomModal && (
        <RoomAccessCard
          onClose={handleCloseModal}
          onCreateRoom={handleCreateRoom}
          onJoinRoom={handleJoinRoom}
        />
      )}
    </>
  )
}
