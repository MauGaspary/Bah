import { useState, useEffect } from 'react'
import '../../../index.css'
import { NotebookText, UsersRound, LogOut } from 'lucide-react';

function SidebarAdm() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 1024) {
        setIsMobileMenuOpen(false)
      }
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  useEffect(() => {
    if (isMobileMenuOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }

    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isMobileMenuOpen])
  return (
    <>
      <div className="sidebar">
        <aside
          id="separator-sidebar"
          className="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0"
          aria-label="Sidebar"
        >
          <div
            className="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800"
            style={{
              fontFamily: 'var(--font-mulish)',
              backgroundColor: 'var(--color-bah-purple)',
              color: 'white',
              borderRadius: '0 var(--radius-card) var(--radius-card) 0',
            }}
          >
            <ul className="h-full flex-col justify-around space-y-2 font-medium">
              <div>
                <li>
                  <a
                    href="/admin/dashboard"
                    className="flex items-center p-2 rounded-lg group"
                  >
                    <img src="/src/assets/logo.png" alt="Logo" style={{width:"150px"}}/>
                  </a>
                </li>
                <li className='pb-2 pt-4'>
                  <span className="flex-1 ms-3 whitespace-nowrap">Menu</span>
                </li>
                  <li
                    className="w-full px-3 font-medium text-white hover:text-bah-green cursor-pointer"
                  >
                    <a href="/admin/iniciativas" className="flex items-center p-4 transition duration-75 rounded-lg group hover:bg-purple-700">
                      <NotebookText />
                      <span className="flex-1 ms-3 whitespace-nowrap">
                        Iniciativas
                      </span>
                    </a>
                  </li>
                  <li
                    className="w-full px-3  font-medium text-white hover:text-bah-green cursor-pointer"
                  >
                    <a href="/admin/usuarios" className="flex items-center p-4 transition duration-75 rounded-lg group hover:bg-purple-700">
                      <UsersRound />
                      <span className="flex-1 ms-3 whitespace-nowrap">
                        Usuários
                      </span>
                    </a>
                  </li>
              </div>

              <li className="fixed bottom-2 z-40 font-medium text-white hover:text-bah-green dark:hover:text-bah-green cursor-pointer" 
                onClick={() => {
                localStorage.removeItem('token');
                window.location.href = '/admin';
              }}>
                <div className="flex items-center gap-8 p-4 transition duration-75 rounded-lg group">
                  {/* stacked labels: name and email */}
                  <div className="flex flex-col">
                    <span className="ms-3 whitespace-nowrap">Admin</span>
                    <span className="ms-3 text-sm text-gray-400 dark:text-gray-400 opacity-90 group-hover:text-bah-green dark:group-hover:text-bah-green">admin@gmail.com</span>
                  </div>

                  <LogOut className='text-error'/>
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
