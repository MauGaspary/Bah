import { SquarePenIcon, Trash2Icon } from 'lucide-react'

import { Button } from '../button'

type ListItemProps = {
  title: string
  description: string
  imageUrl: string
  isLast?: boolean
}

function ListItem({
  title,
  description,
  imageUrl,
  isLast,
}: ListItemProps & { isLast?: boolean }) {
  return (
    <div className="relative w-full last:shadow-none">
      {!isLast && (
        <div className="absolute inset-x-0 bottom-0 h-2 shadow-[0_1px_1px_rgba(0,0,0,0.1)] pointer-events-none "></div>
      )}
      <div className="flex justify-between gap-4 ">
        <div className="pl-8">
          <img
            src={imageUrl}
            alt={title}
            className="w-12 h-12 rounded-full object-cover"
          />
        </div>

        <div className="flex flex-col flex-1 min-w-0">
          <h1 className="text-title3-semibold font-mulish truncate  ">
            {title}
          </h1>
          <p className="text-body-regular font-mulish text-label-secondary line-clamp-2">
            {description}
          </p>
        </div>

        <div className="flex gap-3 self-center pr-16 pb-2">
          <Button
            variant="list"
            className="cursor-pointer border-editar-secondary/60 h-8 min-w-0 px-2 py-1 text-sm flex active:scale-95 "
            onClick={() => console.log('Editar')}
          >
            <SquarePenIcon className="w-4 h-4 text-editar" />
            <span className="text-body-regular font-mulish text-editar ">
              Editar
            </span>
          </Button>

          <Button
            variant="list"
            className="cursor-pointer border-excluir-secondary/60 h-8 min-w-0 px-2 py-1 text-sm flex active:scale-95 active:bg-error"
            onClick={() => console.log('Excluir')}
          >
            <Trash2Icon className="w-4 h-4 text-excluir" />
            <span className="text-body-regular font-mulish text-excluir">
              Excluir
            </span>
          </Button>
        </div>
      </div>
    </div>
  )
}

export default ListItem
