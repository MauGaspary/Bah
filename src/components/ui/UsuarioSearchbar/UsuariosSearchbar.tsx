import { UsuarioInput } from './UsuarioInput'
import { Card, CardHeader} from '../card'
import { Button } from '../button'

import { SearchIcon } from 'lucide-react'

function UsuariosSearchbar() {

  const handleSearch = () => {
    console.log('Buscar')
  }


  return (
    <div className="space-y-6">
        <Card className="rounded-card bg-white shadow-md border border-none ">
          <CardHeader className="flex items-center gap-10 px-10 ">

          <div className="relative w-full rounded-2xl border border-gray-300 focus-within:ring-2 focus-within:ring-bah-purple focus-within:border-transparent">
        <UsuarioInput className="w-full bg-background-secondary rounded-2xl" 
        placeholder="Buscar iniciativa por categoria, palavras-chave, data..."

        onKeyDown={(e) => {
          if(e.key === 'Enter') {
            handleSearch()
          }}}/>

        <Button variant="ghost" 
        className="cursor-pointer active:scale-90 rounded-full absolute right-3 top-1/2 -translate-y-1/2"
        size="icon"
        onClick={() => handleSearch()}>
          <SearchIcon className="w-3 h-3 text-label-secondary" />
        </Button>

        </div>
          <Button className="cursor-pointer bg-success active:scale-95"
          onClick={() => console.log('Novo usuário')}>
            Novo Usuário
            </Button>
           
          </CardHeader>
        </Card>
    </div>  
  )
}

export default UsuariosSearchbar;
