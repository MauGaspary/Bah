import { useState, useRef, useEffect } from 'react'

import type { VariantProps } from 'class-variance-authority'

import { cn } from '@/lib/utils'

import { Button, buttonVariants } from '../button'
import JourneyDescription from './JourneyDescription'

type StageVariant = NonNullable<VariantProps<typeof buttonVariants>['variant']>

const stages: Array<{
  id: string
  title: string
  mobileTitle: string
  variant: StageVariant
  description: string
  actions: string[]
  challenges: string[]
}> = [
  {
    id: 'buscar-conhecimento',
    title: 'Buscar Conhecimento',
    mobileTitle: 'Conhecimento',
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
    mobileTitle: 'Conexões',
    variant: 'error',
    description:
      'Nesta fase, você percebe que precisa se conectar com outras pessoas, especialistas e comunidades que podem acelerar sua jornada. O foco é criar relacionamentos relevantes, trocar conhecimentos e encontrar oportunidades que surgem por meio do networking. As conexões certas podem oferecer direcionamento, apoio e até abrir portas para colaborações importantes.',
    actions: [
      'Participar de eventos, feiras e encontros do setor',
      'Buscar mentores e pessoas mais experientes',
      'Engajar com comunidades, grupos e redes profissionais',
    ],
    challenges: [
      'Dificuldade em encontrar pessoas realmente relevantes',
      'Falta de confiança para iniciar conversas e apresentar sua ideia',
      'Sensação de estar isolado ou desconectado do ecossistema',
    ],
  },
  {
    id: 'conseguir-fundos',
    title: 'Conseguir Fundos',
    mobileTitle: 'Fundos',
    variant: 'primary',
    description:
      'Nesta etapa, você já validou parte da sua ideia e compreende que precisa de recursos financeiros para avançar. O foco é buscar investimentos, programas de apoio, créditos ou iniciativas que possibilitem a evolução do projeto. Aqui, preparar uma boa apresentação e demonstrar o potencial do negócio é essencial.',
    actions: [
      'Preparar pitch, apresentação e materiais para investidores',
      'Mapear fontes de financiamento (investidores, editais, bancos, aceleradoras)',
      'Ajustar o modelo financeiro e projeções do negócio',
    ],
    challenges: [
      'Não saber como falar com investidores',
      'Falta de clareza sobre o valor necessário e como usá-lo',
      'Dificuldade em comprovar números ou apresentar resultados',
    ],
  },
  {
    id: 'operar-e-escalar',
    title: 'Operar e Escalar',
    mobileTitle: 'Escalar',
    variant: 'salmon',
    description:
      'Neste ponto, seu negócio já está em funcionamento, e o foco passa a ser otimizar operações, melhorar processos e aumentar a capacidade de entrega. É a fase de profissionalização: tornar as atividades mais eficientes, gerar previsibilidade e preparar a empresa para crescer sem perder qualidade.',
    actions: [
      'Padronizar processos internos e fluxos de trabalho',
      'Monitorar indicadores de desempenho com regularidade',
      'Implementar ferramentas de gestão e automação',
    ],
    challenges: [
      'Problemas de organização interna e processos falhos',
      'Dificuldade em delegar e construir uma equipe sólida',
      'Falta de previsibilidade financeira e operacional',
    ],
  },
  {
    id: 'capacidades',
    title: 'Capacidades',
    mobileTitle: 'Capacidades',
    variant: 'darkBlue',
    description:
      'Nesta fase, você entende que, para sustentar o crescimento, precisa desenvolver novas habilidades — tanto pessoais quanto da equipe. É um momento de aprimoramento contínuo para fortalecer competências técnicas, estratégicas e comportamentais que permitirão avançar com mais segurança e maturidade.',
    actions: [
      'Desenvolver habilidades de liderança, gestão e tomada de decisão',
      'Criar uma cultura organizacional sólida e alinhada',
      'Incentivar o desenvolvimento da equipe e planos de carreira',
    ],
    challenges: [
      'Falta de tempo para aprender ou se desenvolver',
      'Dificuldade em criar uma cultura forte e engajada',
      'Falta de profissionais capacitados para acompanhar o ritmo',
    ],
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
    border: 'border-error/50',
    stroke: '#ff3b30',
  },
  primary: {
    bg: 'bg-bah-blue',
    border: 'border-bah-blue/80',
    stroke: '#41edee',
  },
  salmon: {
    bg: 'bg-bah-red',
    border: 'border-bah-red/80',
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
  const [descriptionLine, setDescriptionLine] =
    useState<LineCoordinates | null>(null)
  const [descriptionLeft, setDescriptionLeft] = useState<number>(0)
  const [descriptionTop, setDescriptionTop] = useState<number>(0)
  const [descriptionWidth, setDescriptionWidth] = useState<number>(0)
  const timelineContainerRef = useRef<HTMLDivElement>(null)
  const buttonRefs = useRef<(HTMLDivElement | null)[]>([])
  const parentContainerRef = useRef<HTMLDivElement>(null)
  const descriptionRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const updatePositions = () => {
      if (!timelineContainerRef.current || !parentContainerRef.current) return

      const parentRect = parentContainerRef.current.getBoundingClientRect()
      const timelineRect = timelineContainerRef.current.getBoundingClientRect()

      const dotPos = buttonRefs.current.map(buttonRef => {
        if (!buttonRef) return 0
        const buttonRect = buttonRef.getBoundingClientRect()
        const buttonCenterX = buttonRect.left + buttonRect.width / 2
        return ((buttonCenterX - timelineRect.left) / timelineRect.width) * 100
      })
      setDotPositions(dotPos)

      const lines = buttonRefs.current.map(
        (buttonRef, index): LineCoordinates => {
          if (!buttonRef) return { x1: 0, y1: 0, x2: 0, y2: 0 }

          const buttonRect = buttonRef.getBoundingClientRect()
          const dotX =
            (dotPos[index] / 100) * timelineRect.width +
            (timelineRect.left - parentRect.left)

          return {
            x1: buttonRect.left + buttonRect.width / 2 - parentRect.left,
            y1: buttonRect.bottom - parentRect.top,
            x2: dotX,
            y2: timelineRect.top + timelineRect.height / 2 - parentRect.top,
          }
        }
      )
      setLineCoordinates(lines)

      const activeIndex = stages.findIndex(stage => stage.id === active.id)
      if (!descriptionRef.current || dotPos.length === 0 || activeIndex < 0)
        return

      const dotCenterX =
        (dotPos[activeIndex] / 100) * timelineRect.width +
        (timelineRect.left - parentRect.left)
      const isMobile = window.innerWidth < 768
      const calculatedWidth = isMobile
        ? parentRect.width * 0.95
        : parentRect.width * 0.67
      setDescriptionWidth(calculatedWidth)

      let desiredLeft: number
      const totalStages = stages.length

      if (isMobile) {
        desiredLeft = (parentRect.width - calculatedWidth) / 2
      } else if (activeIndex === 0) {
        desiredLeft = 0
      } else if (activeIndex === totalStages - 1) {
        desiredLeft = parentRect.width - calculatedWidth
      } else {
        const progress = activeIndex / (totalStages - 1)
        desiredLeft = (parentRect.width - calculatedWidth) * progress
      }

      const clampedLeft = Math.max(
        0,
        Math.min(parentRect.width - calculatedWidth, desiredLeft)
      )
      setDescriptionLeft(clampedLeft)

      const calculatedTop = timelineRect.bottom - parentRect.top + 32
      setDescriptionTop(calculatedTop)

      const dotCenterY =
        timelineRect.top + timelineRect.height / 2 - parentRect.top
      const descriptionTopY = calculatedTop
      setDescriptionLine({
        x1: dotCenterX,
        y1: dotCenterY + 2,
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
    return (
      variantColors[key as keyof typeof variantColors] || variantColors.primary
    )
  }

  const activeColors = getVariantColors(active.variant)

  return (
    <div className="flex flex-col items-center w-full max-w-4xl mx-auto px-4">
      <div
        ref={parentContainerRef}
        className="relative w-full overflow-visible pb-[650px] md:pb-80"
      >
        <svg className="absolute inset-0 w-full h-full pointer-events-none z-0">
          {lineCoordinates.map((coords, index) => (
            <line
              key={stages[index].id}
              {...coords}
              stroke={
                variantColors[
                  stages[index].variant as keyof typeof variantColors
                ]?.stroke || variantColors.primary.stroke
              }
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

        <div className="relative w-full flex items-end justify-between mb-4 z-10 px-1 md:px-2">
          {stages.map((stage, index) => (
            <div
              key={stage.id}
              ref={el => {
                buttonRefs.current[index] = el
              }}
              className={cn(
                'relative flex flex-col items-center flex-1 min-w-0',
                index % 2 === 0 && 'mb-8 md:mb-16'
              )}
            >
              <Button
                variant={stage.variant}
                className={cn(
                  active.id === stage.id &&
                    'ring-2 ring-offset-2 ring-bah-purple',
                  'text-xs md:text-sm px-1 md:px-4 w-full max-w-[90px] md:max-w-none',
                  'min-w-0',
                  'whitespace-nowrap',
                  'overflow-hidden text-ellipsis md:overflow-visible md:text-clip'
                )}
                onClick={() => setActive(stage)}
              >
                <span className="md:hidden truncate w-full">
                  {stage.mobileTitle}
                </span>
                <span className="hidden md:inline w-full">{stage.title}</span>
              </Button>
            </div>
          ))}
        </div>

        <div
          ref={timelineContainerRef}
          className="relative w-full flex items-center z-10"
        >
          <div className="absolute left-0 w-6 h-6 bg-bah-purple rounded-full -translate-x-1/2 z-10" />
          <div className="w-full h-1 bg-bah-purple" />
          <div className="absolute right-0 w-6 h-6 bg-bah-purple rounded-full translate-x-1/2 z-10" />
          {dotPositions.length > 0 &&
            stages.map((stage, index) => (
              <div
                key={stage.id}
                className="absolute top-1/2 -translate-x-1/2 -translate-y-1/2 flex items-center justify-center pointer-events-none z-20"
                style={{ left: `${dotPositions[index]}%` }}
              >
                <div
                  className={cn(
                    'w-4 h-4 rounded-full',
                    variantColors[stage.variant as keyof typeof variantColors]
                      ?.bg || variantColors.primary.bg
                  )}
                />
              </div>
            ))}
        </div>

        <div
          ref={descriptionRef}
          className="absolute transition-all duration-300 z-10"
          style={{
            left: `${descriptionLeft}px`,
            top: `${descriptionTop}px`,
            width: descriptionWidth > 0 ? `${descriptionWidth}px` : '67%',
          }}
        >
          <JourneyDescription
            active={active}
            borderColor={activeColors.border}
            strokeColor={activeColors.stroke}
          />
        </div>
      </div>
    </div>
  )
}

export default Timeline
