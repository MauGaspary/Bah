import { Input } from './input'
import { Card, CardHeader} from './card'
import { Button } from './button'

import { SearchIcon } from 'lucide-react'

function IniciativasSearchbar() {
  return (
    <div className="space-y-6">
        <Card className="rounded-card bg-white shadow-md border border-stroke-primary ">
          <CardHeader className="flex items-center gap-10 px-10 ">

        <div className="relative flex-1">
        <Input className="w-full bg-background-secondary rounded-lg" 
        placeholder="Buscar iniciativa por categoria, palavras-chave, data..." />

        <Button variant="ghost" 
        className="cursor-pointer active:scale-90 rounded-full absolute right-3 top-1/2 -translate-y-1/2"
        size="icon"
        onClick={() => console.log('Buscar')}>
          <SearchIcon className="w-3 h-3 text-label-secondary" />
        </Button>

        </div>
          <Button className="cursor-pointer bg-success active:scale-95"
          onClick={() => console.log('Nova iniciativa')}>
            Nova iniciativa
            </Button>
           
          </CardHeader>
        </Card>
    </div>
  )
}

export default IniciativasSearchbar;