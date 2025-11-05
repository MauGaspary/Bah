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
}

function JourneyDescription({ active, borderColor }: JourneyDescriptionProps) {
  return (
    <div className="flex flex-col gap-12 w-full ">
      <Card className={`${borderColor} border-2 bg- w-2/3 bg-zinc-300`}>
        <CardContent>
          <p className="text-sm text-muted-foreground">{active.description}</p>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-2/3 ">
        <Card className={`${borderColor} border-2 max-h-64 overflow-y-auto bg-zinc-300`}>
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

        <Card className={`${borderColor} border-2 max-h-64 overflow-y-auto bg-zinc-300`}>
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

