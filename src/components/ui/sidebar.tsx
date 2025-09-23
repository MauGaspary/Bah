import { NotebookText, UsersRound, LogOut } from 'lucide-react'
import React from 'react'
import { NavLink, useNavigate, useLocation } from 'react-router-dom'

import LogoImg from '../../../assets/logo.png'
import '../../../index.css'

function MenuItem({ to, label, Icon}: { to: string; label: string; Icon: React.ComponentType<React.SVGProps<SVGSVGElement>> }) {
  const location = useLocation()
  const isActive = location.pathname === to

  return (
    <li className="w-full">
      <NavLink to={to} className={({ isActive: navIsActive }) => `block -mx-3 transition duration-75 ${navIsActive || isActive ? 'bg-purple-400' : ''}`}>
        <div className={`group flex w-full items-center px-6 py-4 ${isActive ? '' : 'hover:bg-purple-400'}`}>
          <Icon className={`${isActive ? 'text-bah-green' : 'text-white group-hover:text-bah-green'}`} />
          <span className="flex-1 ms-3 whitespace-nowrap">{label}</span>
        </div>
      </NavLink>
    </li>
  )
}

function SidebarAdm() {
  const navigate = useNavigate()

  return (
    <>
      <div className="sidebar">
        <aside
          id="separator-sidebar"
          className="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0"
          aria-label="Sidebar"
        >
          <div
            className="h-full px-3 py-4 overflow-y-auto bg-bah-purple text-white font-mulish rounded-tr-[var(--radius-card)] rounded-br-[var(--radius-card)]"
          >
            <ul className="h-full flex-col justify-around space-y-2 font-medium ">
              <div>
                <li>
                  <NavLink to="/dashboard" className="block -mx-3">
                    <div className="group flex w-full items-center px-6 py-4">
                      <img src={LogoImg} alt="Logo" className="w-[150px]" />
                    </div>
                  </NavLink>
                </li>
                <li className='pb-4 pt-4'>
                  <span className="flex-1 ms-3 whitespace-nowrap">Menu</span>
                </li>
                <MenuItem to="/admin/iniciativas" label="Iniciativas" Icon={NotebookText} />
                <MenuItem to="/admin/usuarios" label="Usuários" Icon={UsersRound} />
              </div>

              <li className="fixed bottom-0 left-0 w-64 font-medium text-white cursor-pointer"
                onClick={() => {
                localStorage.removeItem('token');
                navigate('/admin')
              }}>
                <div className="w-full transition duration-75">
                  <div className="group flex justify-center items-center py-5 gap-8 rounded-br-[var(--radius-card)] hover:bg-purple-400">
                    <div className="flex flex-col">
                      <span className="ms-3 whitespace-nowrap">Admin</span>
                      <span className="ms-3 text-sm text-gray-400 dark:text-gray-400 opacity-90 group-hover:text-bah-green">admin@gmail.com</span>
                    </div>
                    <LogOut className='text-error group-hover:text-bah-green'/>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </aside>
      </div>
    </>
  )
}
export default SidebarAdm