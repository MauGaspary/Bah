import {SquarePenIcon, Trash2Icon} from "lucide-react"

import { Button } from '../button'

type ListItemProps = {
    title: string;
    description: string;
    imageUrl: string;
}

function ListItem({title, description, imageUrl}: ListItemProps) {
    return (
        <div className="relative w-full">
            <div className="absolute inset-x-0 bottom-0 h-2 shadow-[0_1px_1px_rgba(0,0,0,0.1)] pointer-events-none"></div>
        <div className="flex gap-4">

            <div className="pl-8">
                <img src={imageUrl} alt={title} className="w-12 h-12 rounded-full object-cover"/>
            </div>

            <div className="flex flex-col ">
                <h1 className="text-title3-semibold font-mulish  ">{title}</h1>
                <p className="text-body-regular font-mulish text-label-secondary ">{description}</p>
            </div>

            <div className="ml-auto flex gap-2 p-2 ">
                <Button variant="outline" className="cursor-pointer border-bah-blue h-8 min-w-0 px-2 py-1 text-sm flex ">
                    <SquarePenIcon className="w-4 h-4 text-bah-blue" />
                   <p className="text-body-regular font-mulish text-bah-blue ">Editar</p>
                </Button>

                <Button variant="outline" className="cursor-pointer border-error h-8 min-w-0 px-2 py-1 text-sm flex ">
                    <Trash2Icon className="w-4 h-4 text-error" />
                <p className="text-body-regular font-mulish text-error">Excluir</p>
                </Button>

            </div>
        </div>
        </div>
        
    )
}

export default ListItem;