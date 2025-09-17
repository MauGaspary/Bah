
import UsuariosSearchbar from '@/components/ui/UsuariosSearchbar'
import UsuariosList from '@/components/ui/UsuariosList/UsuariosList'

function UsuariosListPage() {
  return ( 
    <div className="min-h-screen bg-background-secondary py-6 pr-6">
        <div className="ml-[20%] justify-start">
        <div className="text-left ">
          <h1 className="text-large-title font-mulish text-bah-purple ">
            Lista de Usuários
          </h1>
          <p className="text-body-regular font-mulish text-label-secondary">
            Gerencie todos usuários do sistema
          </p>
        </div>
            <div className="py-6 pr-6">
                <UsuariosSearchbar />

                <div className="mt-16">
                <UsuariosList />
                </div>

            </div>

        

        </div>
    </div>

    
  )
}

export default UsuariosListPage
