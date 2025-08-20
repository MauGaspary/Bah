import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useNavigate } from 'react-router-dom'

function DashboardPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-background-secondary">
      <div className="max-w-4xl mx-auto space-y-6 p-6">
        {/* Header com botão voltar */}
        <div className="flex items-center justify-between">
          <Button 
            variant="secondary" 
            onClick={() => navigate('/')}
            className="mb-4"
          >
            ← Voltar
          </Button>
        </div>

        {/* Header */}
        <div className="text-center">
          <h1 className="text-large-title font-kanit text-label-primary">
            BAH App
          </h1>
          <p className="text-body-regular font-sf-pro text-label-secondary">
            Aplicação minimalista usando design tokens
          </p>
        </div>

        {/* Example Card */}
        <Card className="rounded-card bg-white shadow-md border border-stroke-primary">
          <CardHeader>
            <CardTitle className="text-title3-semibold font-sf-pro-text text-label-primary">
              Exemplo de Card
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-callout-regular font-sf-pro text-label-primary">
              Este é um exemplo de como usar os design tokens na aplicação.
            </p>

            {/* Buttons */}
            <div className="flex gap-3 flex-wrap">
              <Button variant="primary">Primário</Button>
              <Button variant="success">Sucesso</Button>
              <Button variant="secondary">Secundário</Button>
            </div>

            {/* Custom Component Demo */}
            <div className="space-y-3">
              <h4 className="text-callout-semibold font-sf-pro-text text-black">
                Componentes Customizados:
              </h4>

              <Button
                variant="purple"
                onClick={() => alert('Iniciativas salvas!')}
              >
                Salvar iniciativas
              </Button>

              <Button
                variant="purple"
                onClick={() => alert('Dados exportados!')}
              >
                Exportar dados
              </Button>

              <Button
                variant="purple"
                disabled
                onClick={() => alert('Não deveria executar')}
              >
                Botão Desabilitado
              </Button>
            </div>

            {/* Status indicators */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-success rounded-full"></div>
                <span className="text-footnote font-sf-pro text-label-primary">
                  Online
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-error rounded-full"></div>
                <span className="text-footnote font-sf-pro text-label-primary">
                  Erro
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-bah-blue rounded-full"></div>
                <span className="text-footnote font-sf-pro text-label-primary">
                  BAH
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center pt-4 border-t border-stroke-primary">
          <p className="text-footnote font-sf-pro text-label-tertiary">
            Design System BAH © 2025
          </p>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage