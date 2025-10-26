import { useNavigate } from 'react-router-dom'

import type { IniciativaHorarioResponse } from '@/interfaces/IIniciativas'

import { Badge } from '@/components/badge'

type CardItemProps = {
  id: string
  imageUrl: string
  title: string
  description: string
  horarios: IniciativaHorarioResponse[]
}

const formatTime = (timeString: string): string => {
  return timeString.slice(0, 5)
}

function CardItem(props: CardItemProps) {
  const { id, imageUrl, title, description, horarios } = props
  const navigate = useNavigate()

  const handleClick = () => {
    navigate(`/iniciativa/${id}`)
  }

  return (
    <div className="relative w-full">
      <div
        onClick={handleClick}
        className="flex gap-4 bg-background-secondary rounded-4xl cursor-pointer hover:opacity-90 transition-opacity"
      >
        <div className="flex-shrink-0">
          <img
            src={imageUrl}
            alt={props.title}
            className="w-48 h-48 rounded-l-4xl object-cover"
          />
        </div>

        <div className="flex flex-col justify-between flex-1 min-w-0 py-4">
          <div>
            <h1 className="text-title3-semibold font-mulish truncate">
              {title}
            </h1>
            <p className="text-subheadline-regular font-mulish text-label-secondary line-clamp-4">
              {description}
            </p>
          </div>

          <div className="flex w-full flex-nowrap gap-2 overflow-x-auto">
            {horarios.map((horario, index) => (
              <Badge
                key={horario.id || index}
                className="bg-bah-green flex"
                variant="default"
              >
                {formatTime(horario.hora_inicio)} -{' '}
                {formatTime(horario.hora_fim)}
              </Badge>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default CardItem
