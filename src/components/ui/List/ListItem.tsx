import { SquarePenIcon, Trash2Icon } from 'lucide-react'
import { Button } from '../button'

type BaseProps = {
  imageUrl: string
  isLast?: boolean
  isDeleting?: boolean
  onEdit?: () => void
  onDelete?: () => void
}

type DefaultVariant = {
  variant?: 'default'
  title: string
  description: string
}

type UsuarioVariant = {
  variant: 'usuario'
  title: string
  email: string
}

type ListItemProps = BaseProps & (DefaultVariant | UsuarioVariant)

function ListItem(props: ListItemProps) {
  const { imageUrl, isLast, isDeleting, onEdit, onDelete } = props

  return (
    <div className="relative w-full last:shadow-none">
      {!isLast && (
        <div className="absolute inset-x-0 bottom-0 h-2 shadow-[0_1px_1px_rgba(0,0,0,0.1)] pointer-events-none" />
      )}

      <div className="flex justify-between gap-4 items-center">
        <div className="pl-8 flex items-center">
          <img
            src={imageUrl}
            alt={props.title}
            className="w-12 h-12 rounded-full object-cover"
          />
        </div>

        <div className="flex flex-col flex-1 min-w-0">
          <h1 className="text-title3-semibold font-mulish truncate">
            {props.title}
          </h1>

          {props.variant === 'usuario' ? (
            <p className="text-body-regular font-mulish text-label-secondary line-clamp-2 underline decoration-label-secondary/50">
              {props.email}
            </p>
          ) : (
            <p className="text-body-regular font-mulish text-label-secondary line-clamp-2">
              {props.description}
            </p>
          )}
        </div>

        <div className="flex gap-3 self-center pr-16 pb-2">
          <Button
            variant="list"
            className="cursor-pointer border-editar-secondary/60 h-8 min-w-0 px-2 py-1 text-sm flex active:scale-95"
            onClick={onEdit}
          >
            <SquarePenIcon className="w-4 h-4 text-editar" />
            <span className="text-body-regular font-mulish text-editar">
              Editar
            </span>
          </Button>

          <Button
            variant="list"
            className="cursor-pointer border-excluir-secondary/60 h-8 min-w-0 px-2 py-1 text-sm flex active:scale-95 active:bg-error"
            onClick={onDelete}
            disabled={isDeleting}
          >
            <Trash2Icon className="w-4 h-4 text-excluir" />
            <span className="text-body-regular font-mulish text-excluir">
              {isDeleting ? 'Excluindo...' : 'Excluir'}
            </span>
          </Button>
        </div>
      </div>
    </div>
  )
}

export default ListItem
