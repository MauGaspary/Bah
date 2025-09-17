import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'


import { optionsItems } from './NavigationItems'
import '../../../index.css'

function SidebarAdm() {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
    const [isScrolled, setIsScrolled] = useState(false)
  
    const navigate = useNavigate()
  
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
  
    useEffect(() => {
      const homeSection = document.getElementById('home-section')
  
      if (!homeSection) {
        setIsScrolled(true)
        return
      }
  
      const observer = new IntersectionObserver(
        ([entry]) => {
          setIsScrolled(!entry.isIntersecting)
        },
        { threshold: 0, rootMargin: '-20px 0px 0px 0px' }
      )
  
      observer.observe(homeSection)
      return () => observer.disconnect()
    }, [])
  
    const handleNavigation = (path: string) => {
      navigate(path)
      setIsMobileMenuOpen(false)
    }
  return (
    <>
      <div className="sidebar">
        <aside id="separator-sidebar" className="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0" aria-label="Sidebar">
          <div className="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800" 
          style={{
            fontFamily: 'var(--font-kanit)',
            backgroundColor: 'var(--color-bah-purple)',
            color: 'white',
            fontWeight: 'bold',
            borderRadius: '0 var(--radius-card) var(--radius-card) 0',
          }}>
            <ul className="space-y-2 font-medium">
              <li>
                <a href="/admin/dashboard" className="flex items-center p-2 rounded-lg group">
                  <img
                    src="/src/assets/bah-bg-purple.png"
                    alt="Logo"
                  />  
                </a>
              </li>
              <li>
                <span className="flex-1 ms-3 whitespace-nowrap">Menu</span>
              </li>
              {optionsItems.map(item => (
                <li
                  key={item.id}
                  onClick={() => handleNavigation(item.path)}
                  className="w-full px-3 py-2  font-medium text-white hover:text-bah-green cursor-pointer transition-all duration-300 ease-in-out hover:-translate-y-1"
                >
                  <a className="flex items-center p-4 transition duration-75 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 group hover:bg-purple-700">
                    <svg className="shrink-0 w-5 h-5 transition duration-75" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18"> 
                      <path d={item.pathData} />
                    </svg>
                    <span className="flex-1 ms-3 whitespace-nowrap">{item.label}</span>
                  </a>
                </li>
              ))}
              <li className="fixed bottom-10 z-40 w-full px-4 py-2  font-medium text-white hover:text-bah-green cursor-pointer transition-all duration-300 ease-in-out hover:-translate-y-1">
                  <a href="#" className="flex items-center p-4 transition duration-75 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 group hover:bg-purple-700">
                    <span className="flex-1 ms-3 whitespace-nowrap">Admin<br />admin@gmail.com</span>
                    <svg className="shrink-0 w-5 h-5 transition duration-75 text-bah-red group-hover:text-red-500 dark:group-hover:text-crimson" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 18 16">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 8h11m0 0L8 4m4 4-4 4m4-11h3a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-3"/>
                    </svg>
                  </a>
              </li>
            </ul>
          </div>
        </aside>
      </div>
    </>
  )
}
export default SidebarAdm