import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '../../../../../../../../vite.svg'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="max-w-2xl mx-auto text-center space-y-8">
        <div className="flex justify-center items-center gap-8">
          <a href="https://vite.dev" target="_blank" rel="noopener noreferrer">
            <img
              src={viteLogo}
              className="h-16 w-16 hover:scale-110 transition-transform"
              alt="Vite logo"
            />
          </a>
          <a href="https://react.dev" target="_blank" rel="noopener noreferrer">
            <img
              src={reactLogo}
              className="h-16 w-16 hover:scale-110 transition-transform animate-spin-slow"
              alt="React logo"
            />
          </a>
        </div>

        <h1 className="text-4xl font-bold text-foreground">
          Vite + React + Tailwind + shadcn/ui
        </h1>

        <Card className="w-full max-w-md mx-auto">
          <CardHeader>
            <CardTitle>Contador</CardTitle>
            <CardDescription>
              Clique no botão para incrementar o contador
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Button
              onClick={() => setCount((count) => count + 1)}
              className="w-full"
              size="lg"
            >
              count is {count}
            </Button>
            <p className="text-sm text-muted-foreground">
              Edite{' '}
              <code className="bg-muted px-1 py-0.5 rounded text-xs">
                src/App.tsx
              </code>{' '}
              e salve para testar o HMR
            </p>
          </CardContent>
        </Card>

        <p className="text-muted-foreground">
          Clique nos logos do Vite e React para saber mais
        </p>
      </div>
    </div>
  )
}

export default App
