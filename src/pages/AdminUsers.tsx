import UsuariosList from '@/components/ui/List/UsuariosList'
import AdminSearchbar from '@/components/ui/AdminSearchbar/AdminSearchbar'
import SidebarAdm from '@/components/ui/sidebar'

function AdminUsuarios() {
  return (
    <div>
      <div className="min-h-screen flex bg-background-secondary">
        <div className="fixed top-0 left-0 h-screen">
          <SidebarAdm />
        </div>

        <main className="flex-1 ml-[20%] py-6 pr-6 pl-6">
          <div className="text-left ">
            <h1 className="text-large-title font-mulish text-bah-purple ">
              Lista de Usuários
            </h1>
            <p className="text-body-regular font-mulish text-label-secondary">
              Gerencie todos usuários do sistema
            </p>
          </div>

          <div className="py-6 pr-6">
            <AdminSearchbar
              placeholder="Buscar usuários por nome, email, região..."
              buttonLabel="Novo usuário"
              onButtonClick={() => console.log('Novo usuário')}
              onSearchChange={(searchValue: string) => {
                // Implementar busca no futuro
                console.log('Buscar:', searchValue)
              }}
            />

            <div className="mt-8">
              <UsuariosList />
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default AdminUsuarios
