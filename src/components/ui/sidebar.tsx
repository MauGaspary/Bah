import { NotebookText, UsersRound, LogOut } from 'lucide-react'
import { useState } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import LogoImg from '../../assets/logo.png'
import '../../index.css'
import { removeToken } from '../../lib/auth'
import Modal from '../logoutModal'

interface MenuItemProps {
  to: string
  label: string
  Icon: React.ComponentType<React.SVGProps<SVGSVGElement>>
}

function MenuItem({ to, label, Icon }: MenuItemProps) {
  return (
    <li className="w-full">
      <NavLink
        to={to}
        className={({ isActive }) =>
          `block -mx-3 transition duration-75 ${isActive ? 'bg-purple-400' : ''}`
        }
      >
        {({ isActive }) => (
          <div className="group flex w-full items-center px-8 py-4">
            <Icon
              className={`${
                isActive
                  ? 'text-bah-green'
                  : 'text-white group-hover:text-bah-green'
              }`}
            />
            <span className="flex-1 ms-3 whitespace-nowrap">{label}</span>
          </div>
        )}
      </NavLink>
    </li>
  )
}

function SidebarAdm() {
  const [logoutPopup, setLogoutPopup] = useState(false)
  const navigate = useNavigate()

  const handleLogout = () => {
    removeToken()
    navigate('/admin')
  }

  return (
    <>
      <div className="sidebar">
        <aside
          id="separator-sidebar"
          className="top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0"
          aria-label="Sidebar"
        >
          <div className="h-full px-3 py-4 overflow-y-auto bg-bah-purple text-white font-mulish rounded-tr-[var(--radius-card)] rounded-br-[var(--radius-card)] flex flex-col">
            <div className="flex-1">
              <ul className="space-y-2 font-medium">
                <li>
                  <NavLink to="/dashboard" className="block -mx-3">
                    <div className="group flex w-full items-center px-6 py-4">
                      <img src={LogoImg} alt="Logo" className="w-[150px]" />
                    </div>
                  </NavLink>
                </li>
                <li className="pb-4 pt-4">
                  <span className="flex-1 ms-3 whitespace-nowrap">Menu</span>
                </li>
                <MenuItem
                  to="/admin/iniciativas"
                  label="Iniciativas"
                  Icon={NotebookText}
                />
                <MenuItem
                  to="/admin/usuarios"
                  label="Usuários"
                  Icon={UsersRound}
                />
              </ul>
            </div>

            <div className="font-medium text-white">
              <div className="flex items-center justify-between px-3 py-2">
                <div className="flex flex-col">
                  <span className="whitespace-nowrap">Admin</span>
                  <span className="text-sm text-gray-400 opacity-90">
                    admin@gmail.com
                  </span>
                </div>
                <button
                  onClick={() => setLogoutPopup(true)}
                  className="p-2 text-red-400 hover:text-bah-green rounded transition duration-75 cursor-pointer"
                >
                  <LogOut size={24} />
                </button>
              </div>
            </div>
          </div>
        </aside>
      </div>

      {logoutPopup && (
        <Modal onClose={() => setLogoutPopup(false)}>
          <div className="bg-white rounded-[var(--radius-card)] text-center shadow-lg w-96 p-10">
            <h2 className="text-xl font-bold mb-4">Logout</h2>
            <p className="mb-4">Tem certeza que deseja fazer logout?</p>
            <div className="flex justify-center gap-4">
              <button
                onClick={handleLogout}
                className="flex-1 px-6 py-3 bg-bah-purple text-white rounded-[var(--radius-button)] hover:bg-purple-700 transition-colors cursor-pointer"
              >
                Sim
              </button>
              <button
                onClick={() => setLogoutPopup(false)}
                className="flex-1 px-6 py-3 bg-white text-black rounded-[var(--radius-button)] border border-gray-300 hover:shadow-md transition-shadow cursor-pointer"
              >
                Cancelar
              </button>
            </div>
          </div>
        </Modal>
      )}
    </>
  )
}

export default SidebarAdm
