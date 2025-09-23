import SidebarAdm from '@/components/ui/sidebar'

function AdminIniciativas() {
  return (
    <div className="flex">
      <SidebarAdm />
      <div className="flex-grow p-6" style={{ marginLeft: '256px' }}>
        <h1 className="text-2xl font-bold mb-4">Admin Iniciativas Page</h1>
        {/* Conteúdo da página de Admin Iniciativas */}
      </div>
    </div>
  )
}
export default AdminIniciativas