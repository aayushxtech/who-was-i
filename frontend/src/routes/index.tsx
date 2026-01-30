import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/')({ component: App })

function App() {

  return (
    <>
    <div>
      Hello, The first addition of who was i.....
    </div>
    <div className='text-red-500'>
      I can guarrente you that this wont be just two lines of code after this.
    </div>
    </>
  )
}
