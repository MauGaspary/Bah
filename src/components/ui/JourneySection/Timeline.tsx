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

type LineCoordinates = { x1: number; y1: number; x2: number; y2: number }

const variantColors = {
  success: {
    bg: 'bg-bah-green',
    border: 'border-bah-green',
    stroke: '#c7d871',
  },
  error: {
    bg: 'bg-error',
    border: 'border-error',
    stroke: '#ff3b30',
  },
  primary: {
    bg: 'bg-bah-blue',
    border: 'border-bah-blue',
    stroke: '#41edee',
  },
  salmon: {
    bg: 'bg-bah-red',
    border: 'border-bah-red',
    stroke: '#fe716f',
  },
  darkBlue: {
    bg: 'bg-bah-dark-blue',
    border: 'border-bah-dark-blue',
    stroke: '#98a1cc',
  },
} as const

function Timeline() {
  const [active, setActive] = useState(stages[0])
  const [dotPositions, setDotPositions] = useState<number[]>([])
  const [lineCoordinates, setLineCoordinates] = useState<LineCoordinates[]>([])
  const [descriptionLine, setDescriptionLine] = useState<LineCoordinates | null>(null)
  const [descriptionLeft, setDescriptionLeft] = useState<number>(0)
  const timelineContainerRef = useRef<HTMLDivElement>(null)
  const buttonRefs = useRef<(HTMLDivElement | null)[]>([])
  const parentContainerRef = useRef<HTMLDivElement>(null)
  const descriptionRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const updatePositions = () => {
      if (!timelineContainerRef.current || !parentContainerRef.current) return

      const parentRect = parentContainerRef.current.getBoundingClientRect()
      const timelineRect = timelineContainerRef.current.getBoundingClientRect()

      // Calculate dot positions (percentages relative to timeline)
      const dotPos = buttonRefs.current.map((buttonRef) => {
        if (!buttonRef) return 0
        const buttonRect = buttonRef.getBoundingClientRect()
        const buttonCenterX = buttonRect.left + buttonRect.width / 2
        return ((buttonCenterX - timelineRect.left) / timelineRect.width) * 100
      })
      setDotPositions(dotPos)

      // Calculate button-to-dot line coordinates
      const lines = buttonRefs.current.map((buttonRef, index): LineCoordinates => {
        if (!buttonRef) return { x1: 0, y1: 0, x2: 0, y2: 0 }
        
        const buttonRect = buttonRef.getBoundingClientRect()
        const dotX = (dotPos[index] / 100) * timelineRect.width + (timelineRect.left - parentRect.left)
        
        return {
          x1: buttonRect.left + buttonRect.width / 2 - parentRect.left,
          y1: buttonRect.bottom - parentRect.top,
          x2: dotX,
          y2: timelineRect.top + timelineRect.height / 2 - parentRect.top,
        }
      })
      setLineCoordinates(lines)

      // Calculate JourneyDescription position and vertical line
      const activeIndex = stages.findIndex((stage) => stage.id === active.id)
      if (!descriptionRef.current || dotPos.length === 0 || activeIndex < 0) return

      const descriptionRect = descriptionRef.current.getBoundingClientRect()
      const dotCenterX = (dotPos[activeIndex] / 100) * timelineRect.width + (timelineRect.left - parentRect.left)
      const descriptionWidth = descriptionRect.width || parentRect.width * 0.67
      
      // Position description centered on dot, clamped to bounds
      const desiredLeft = dotCenterX - descriptionWidth / 2
      const clampedLeft = Math.max(0, Math.min(parentRect.width - descriptionWidth, desiredLeft))
      setDescriptionLeft(clampedLeft)

      // Vertical line from dot bottom to description top
      const dotBottomY = timelineRect.top + timelineRect.height / 2 + 2 - parentRect.top
      const descriptionTopY = timelineRect.bottom - parentRect.top + 32
      setDescriptionLine({
        x1: dotCenterX,
        y1: dotBottomY,
        x2: dotCenterX,
        y2: descriptionTopY,
      })
    }

    const timeoutId = setTimeout(updatePositions, 0)
    window.addEventListener('resize', updatePositions)
    return () => {
      clearTimeout(timeoutId)
      window.removeEventListener('resize', updatePositions)
    }
  }, [active])

  const getVariantColors = (variant: StageVariant) => {
    const key = variant || 'primary'
    return variantColors[key as keyof typeof variantColors] || variantColors.primary
  }

  const activeColors = getVariantColors(active.variant)

  return (
    <div className="flex flex-col items-center w-full max-w-4xl mx-auto">
      {/* Single parent container for buttons, timeline, description, and connectors */}
      <div ref={parentContainerRef} className="relative w-full">
        {/* SVG overlay for connecting lines - covers entire container */}
        <svg
          className="absolute inset-0 w-full h-full pointer-events-none z-0"
        >
          {lineCoordinates.map((coords, index) => (
            <line
              key={stages[index].id}
              {...coords}
              stroke={variantColors[stages[index].variant as keyof typeof variantColors]?.stroke || variantColors.primary.stroke}
              strokeWidth={2}
              strokeDasharray="4 4"
            />
          ))}
          {descriptionLine && (
            <line
              {...descriptionLine}
              stroke={activeColors.stroke}
              strokeWidth={2}
              strokeDasharray="4 4"
            />
          )}
        </svg>

        {/* Buttons container */}
        <div className="relative w-full flex items-end justify-between mb-4 z-10">
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

        {/* Timeline container */}
        <div ref={timelineContainerRef} className="relative w-full flex items-center z-10">
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
                  className={`w-4 h-4 ${variantColors[stage.variant as keyof typeof variantColors]?.bg || variantColors.primary.bg} rounded-full`}
                />
              </div>
            ))}
        </div>

        {/* JourneyDescription positioned based on active button */}
        <div
          ref={descriptionRef}
          className="relative w-full mt-8 transition-all duration-300 z-10"
          style={{ left: `${descriptionLeft}px` }}
        >
          <JourneyDescription active={active} borderColor={activeColors.border} />
        </div>
      </div>
    </div>
  )
}

export default Timeline
