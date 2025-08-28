import { useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-background-secondary">
      <div className="max-w-4xl mx-auto space-y-6 p-6">
        <div className="text-center">
          <h1 className="text-large-title font-kanit text-label-primary">
            BAH App
          </h1>
          <p className="text-body-regular font-sf-pro text-label-secondary">
            Aplicação minimalista usando design tokens
          </p>
        </div>

        <Card className="rounded-card bg-white shadow-md border border-stroke-primary">
          <CardHeader>
            <CardTitle className="text-title3-semibold font-sf-pro-text text-label-primary">
              Navegação
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-3 flex-wrap">
              <Button
                variant="primary"
                onClick={() => navigate('/dashboard')}
                className="cursor-pointer"
              >
                Ir para Dashboard
              </Button>
            </div>
          </CardContent>
        </Card>

        <div className="text-center pt-4 border-t border-stroke-primary">
          <p className="text-footnote font-sf-pro text-label-tertiary">
            Design System BAH © 2025
          </p>
        </div>
      </div>
    </div>
  )
}

export default HomePage
