import { useState } from 'react'

import { Button, buttonVariants } from '../button'
import { Card, CardContent, CardHeader, CardTitle } from '../card'

import type { VariantProps } from 'class-variance-authority'

type StageVariant = NonNullable<VariantProps<typeof buttonVariants>['variant']>

const stages: Array<{
  id: string
  title: string
  variant: StageVariant
  description: string
  actions: string[]
  challenges: string[]
}> = [
  {
    id: 'buscar-conhecimento',
    title: 'Buscar Conhecimento',
    variant: 'success',
    description:
      'Você está começando sua jornada e percebe que precisa de mais conhecimento para desenvolver sua ideia. Nesta fase, o foco é observar informações e entender melhor o mercado e as possibilidades.',
    actions: [
      'Estruturar equipe e processos',
      'Expandir para novos mercados',
      'Buscar parcerias estratégicas',
      'Implementar métricas de crescimento',
    ],
    challenges: [
      'Não sei por onde começar',
      'Meu esforço não está sendo suficiente',
      'Não encontro soluções para meu problema',
    ],
  },
  {
    id: 'conexoes',
    title: 'Conexões',
    variant: 'error',
    description: '',
    actions: [''],
    challenges: [''],
  },
  {
    id: 'conseguir-fundos',
    title: 'Conseguir Fundos',
    variant: 'primary',
    description: '',
    actions: [''],
    challenges: [''],
  },
  {
    id: 'operar-e-escalar',
    title: 'Operar e Escalar',
    variant: 'salmon',
    description: '',
    actions: [''],
    challenges: [''],
  },
  {
    id: 'desenvolver-capacidades',
    title: 'Desenvolver Capacidades',
    variant: 'darkBlue',
    description: '',
    actions: [''],
    challenges: [''],
  },
]

function Timeline() {
  const [active, setActive] = useState(stages[0])

  const getBorderColor = (variant: StageVariant) => {
    const variantMap: Record<string, string> = {
      success: 'border-bah-green',
      error: 'border-error',
      primary: 'border-bah-blue',
      salmon: 'border-bah-red',
      darkBlue: 'border-bah-dark-blue',
    }
    return variantMap[variant || 'primary'] || 'border-bah-blue'
  }

  const borderColor = getBorderColor(active.variant)

  return (
    <div className="flex flex-col items-center w-full max-w-4xl mx-auto gap-8">
      <div className="relative w-full flex items-end justify-between mb-4">
        {stages.map((stage, index) => (
          <div
            key={stage.id}
            className={`relative flex flex-col items-center ${index % 2 === 0 ? 'mb-16' : ''}`}
          >
            <Button
              variant={stage.variant}
              className={
                active.id === stage.id
                  ? 'ring-2 ring-offset-2 ring-bah-purple'
                  : ''
              }
              onClick={() => setActive(stage)}
            >
              {stage.title}
            </Button>
          </div>
        ))}
      </div>

      <div className="relative w-full flex items-center">
        <div className="absolute left-0 w-6 h-6 bg-bah-purple rounded-full -translate-x-1/2 z-10"></div>
        <div className="w-full h-1 bg-bah-purple"></div>
        <div className="absolute right-0 w-6 h-6 bg-bah-purple rounded-full translate-x-1/2 z-10"></div>
      </div>

      <div className="flex flex-col gap-4 w-full">
        <Card className={`${borderColor} border-2 bg- w-2/3`}>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              {active.description || 'Nenhuma descrição disponível.'}
            </p>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-2/3">
          <Card className={`${borderColor} border-2 max-h-64 overflow-y-auto`}>
            <CardHeader>
              <CardTitle>Suas ações nesta fase:</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="text-sm text-muted-foreground space-y-2">
                {active.actions &&
                active.actions.length > 0 &&
                active.actions[0] ? (
                  active.actions.map((action, index) => (
                    <li key={index} className="list-disc list-inside">
                      {action}
                    </li>
                  ))
                ) : (
                  <li>Nenhuma ação disponível.</li>
                )}
              </ul>
            </CardContent>
          </Card>

          <Card className={`${borderColor} border-2 max-h-64 overflow-y-auto`}>
            <CardHeader>
              <CardTitle>Desafios comuns:</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="text-sm text-muted-foreground space-y-2">
                {active.challenges &&
                active.challenges.length > 0 &&
                active.challenges[0] ? (
                  active.challenges.map((challenge, index) => (
                    <li key={index} className="list-disc list-inside">
                      {challenge}
                    </li>
                  ))
                ) : (
                  <li>Nenhum desafio disponível.</li>
                )}
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default Timeline
