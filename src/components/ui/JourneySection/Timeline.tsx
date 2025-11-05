import { useState, useRef, useEffect } from 'react'

import { Button, buttonVariants } from '../button'

import JourneyDescription from './JourneyDescription'

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

const dotColors: Record<string, string> = {
  success: 'bg-bah-green',
  error: 'bg-error',
  primary: 'bg-bah-blue',
  salmon: 'bg-bah-red',
  darkBlue: 'bg-bah-dark-blue',
}

function Timeline() {
  const [active, setActive] = useState(stages[0])
  const [dotPositions, setDotPositions] = useState<number[]>([])
  const timelineContainerRef = useRef<HTMLDivElement>(null)
  const buttonRefs = useRef<(HTMLDivElement | null)[]>([])

  useEffect(() => {
    const updateDotPositions = () => {
      if (!timelineContainerRef.current) return

      const timelineContainerRect = timelineContainerRef.current.getBoundingClientRect()
      
      const positions = buttonRefs.current.map((buttonRef) => {
        if (!buttonRef) return 0
        const buttonRect = buttonRef.getBoundingClientRect()
        // Calculate the center of the button relative to the timeline container
        const buttonCenterX = buttonRect.left + buttonRect.width / 2
        const relativePosition = ((buttonCenterX - timelineContainerRect.left) / timelineContainerRect.width) * 100
        return relativePosition
      })
      setDotPositions(positions)
    }

    // Use a small delay to ensure DOM is fully rendered
    const timeoutId = setTimeout(updateDotPositions, 0)
    window.addEventListener('resize', updateDotPositions)
    return () => {
      clearTimeout(timeoutId)
      window.removeEventListener('resize', updateDotPositions)
    }
  }, [])

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
            ref={(el) => {
              buttonRefs.current[index] = el
            }}
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

      <div ref={timelineContainerRef} className="relative w-full flex items-center">
        <div className="absolute left-0 w-6 h-6 bg-bah-purple rounded-full -translate-x-1/2 z-10"></div>
        <div className="w-full h-1 bg-bah-purple"></div>
        <div className="absolute right-0 w-6 h-6 bg-bah-purple rounded-full translate-x-1/2 z-10"></div>
        {dotPositions.length > 0 &&
          stages.map((stage, index) => (
            <div
              key={stage.id}
              className="absolute top-1/2 -translate-x-1/2 -translate-y-1/2 flex items-center justify-center pointer-events-none z-20"
              style={{ left: `${dotPositions[index]}%` }}
            >
              <div
                className={`w-4 h-4 ${dotColors[stage.variant] || 'bg-bah-blue'} rounded-full`}
              ></div>
            </div>
          ))}
      </div>

      <JourneyDescription active={active} borderColor={borderColor} />
    </div>
  )
}

export default Timeline
