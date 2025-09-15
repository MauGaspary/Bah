import { Input } from './input'
import { Card, CardHeader} from './card'
import { Button } from './button'

function IniciativasSearchbar() {
  return (
    <div className="space-y-6">
        <Card className="rounded-card bg-white shadow-md border border-stroke-primary ">
          <CardHeader className="flex items-center gap-10 px-10 ">
      
        <Input className="w-full bg-background-secondary" 
        placeholder="Buscar iniciativa por categoria, palavras-chave, data..." />

          <Button className="cursor-pointer bg-success">
            Nova iniciativa
            </Button>
           
          </CardHeader>
        </Card>
    </div>
  )
}

export default IniciativasSearchbar;