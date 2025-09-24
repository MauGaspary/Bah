import SidebarAdm from '@/components/ui/sidebar'
import UsuariosSearchbar from '@/components/ui/UsuarioSearchbar/UsuariosSearchbar'
import UsuariosList from '@/components/ui/UsuariosList/UsuariosList'

function AdminUsuarios() {
  return ( 
    <div className="min-h-screen flex bg-background-secondary py-6 pr-6">
      <div className="fixed top-0 left-0 h-screen">
        <SidebarAdm />
      </div>
        <main className="flex-1 ml-[20%]">
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

        

        </main>
    </div>

    
  )
}

export default AdminUsuarios
