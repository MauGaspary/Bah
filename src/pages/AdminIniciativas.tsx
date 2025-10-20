import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import IniciativasList from '@/components/ui/List/IniciativasList'
import AdminSearchbar from '@/components/ui/AdminSearchbar/AdminSearchbar'
import SidebarAdm from '@/components/ui/sidebar'

function AdminIniciativas() {
  const navigate = useNavigate()
  const [searchTerm, setSearchTerm] = useState('')

  return (
    <div>
      <div className="min-h-screen flex bg-background-secondary">
        <div className="fixed top-0 left-0 h-screen">
          <SidebarAdm />
        </div>

        <main className="flex-1 ml-[20%] py-6 pr-6 pl-6">
          <div className="text-left">
            <h1 className="text-large-title font-mulish text-bah-purple">
              Lista de Iniciativas
            </h1>
            <p className="text-body-regular font-mulish text-label-secondary">
              Gerencie todas iniciativas do sistema
            </p>
          </div>

          <div className="py-6 pr-6">
            <AdminSearchbar
              placeholder="Buscar iniciativa por categoria, palavras-chave, data..."
              buttonLabel="Nova iniciativa"
              onSearchChange={setSearchTerm}
              onButtonClick={() => navigate('/admin/criarIniciativa')}
            />

            <div className="mt-16">
              <IniciativasList searchQuery={searchTerm} />
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default AdminIniciativas
