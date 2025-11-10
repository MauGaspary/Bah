import { useRef, useEffect, useState } from 'react'

import { Card, CardContent, CardHeader, CardTitle } from '../card'

type Stage = {
  id: string
  title: string
  variant: string
  description: string
  actions: string[]
  challenges: string[]
}

type JourneyDescriptionProps = {
  active: Stage
  borderColor: string
  strokeColor: string
}

type LineCoordinates = { x1: number; y1: number; x2: number; y2: number }

function JourneyDescription({
  active,
  borderColor,
  strokeColor,
}: JourneyDescriptionProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const mainCardRef = useRef<HTMLDivElement>(null)
  const actionsCardRef = useRef<HTMLDivElement>(null)
  const challengesCardRef = useRef<HTMLDivElement>(null)
  const [line1, setLine1] = useState<LineCoordinates | null>(null)
  const [line2, setLine2] = useState<LineCoordinates | null>(null)

  useEffect(() => {
    const updateLines = () => {
      if (
        !containerRef.current ||
        !mainCardRef.current ||
        !actionsCardRef.current ||
        !challengesCardRef.current
      ) {
        return
      }

      const containerRect = containerRef.current.getBoundingClientRect()
      const mainCardRect = mainCardRef.current.getBoundingClientRect()
      const actionsCardRect = actionsCardRef.current.getBoundingClientRect()
      const challengesCardRect =
        challengesCardRef.current.getBoundingClientRect()

      const actionsCardCenterX =
        actionsCardRect.left + actionsCardRect.width / 2 - containerRect.left
      const actionsCardTopY = actionsCardRect.top - containerRect.top
      const mainCardBottomY = mainCardRect.bottom - containerRect.top

      const challengesCardCenterX =
        challengesCardRect.left +
        challengesCardRect.width / 2 -
        containerRect.left
      const challengesCardTopY = challengesCardRect.top - containerRect.top

      setLine1({
        x1: actionsCardCenterX,
        y1: actionsCardTopY,
        x2: actionsCardCenterX,
        y2: mainCardBottomY,
      })

      setLine2({
        x1: challengesCardCenterX,
        y1: challengesCardTopY,
        x2: challengesCardCenterX,
        y2: mainCardBottomY,
      })
    }

    const timeoutId = setTimeout(updateLines, 0)
    window.addEventListener('resize', updateLines)
    return () => {
      clearTimeout(timeoutId)
      window.removeEventListener('resize', updateLines)
    }
  }, [active])

  return (
    <div ref={containerRef} className="relative flex flex-col gap-6 md:gap-12 w-full">
      <svg className="absolute inset-0 w-full h-full pointer-events-none z-0">
        {line1 && (
          <line
            {...line1}
            stroke={strokeColor}
            strokeWidth={2}
            strokeDasharray="4 4"
          />
        )}
        {line2 && (
          <line
            {...line2}
            stroke={strokeColor}
            strokeWidth={2}
            strokeDasharray="4 4"
          />
        )}
      </svg>

      <Card
        ref={mainCardRef}
        className={`${borderColor} border-2 bg- w-full bg-zinc-300 relative z-10`}
      >
        <CardContent>
          <p className="text-sm text-muted-foreground">{active.description}</p>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-8 w-full relative z-10">
        <Card
          ref={actionsCardRef}
          className={`${borderColor} border-2 max-h-64 overflow-y-auto bg-zinc-300`}
        >
          <CardHeader>
            <CardTitle>Suas ações nesta fase:</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="text-sm text-muted-foreground space-y-2">
              {active.actions.map((action, index) => (
                <li key={index} className="list-disc list-inside">
                  {action}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card
          ref={challengesCardRef}
          className={`${borderColor} border-2 max-h-64 overflow-y-auto bg-zinc-300`}
        >
          <CardHeader>
            <CardTitle>Desafios comuns:</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="text-sm text-muted-foreground space-y-2">
              {active.challenges.map((challenge, index) => (
                <li key={index} className="list-disc list-inside">
                  {challenge}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default JourneyDescription
