import SidebarAdm from '@/components/ui/sidebar'

function AdminUsuarios() {
  return (
    <div className="flex">
      <SidebarAdm />
      <div className="flex-grow p-6">
        <h1 className="text-2xl font-bold mb-4">Admin Usuarios Page</h1>
      </div>
    </div>
  )
}
export default AdminUsuarios