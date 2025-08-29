import { useState, useEffect } from 'react'

import { Input } from '../Searchbar/Searchbar'

interface HeaderProps {
  variant?: 'default' | 'secondary' | 'custom'
  logo?: string
  customColors?: {
    headerBg?: string
    searchIconMobile?: string
    searchIconDesktop?: string
    buttonHover?: string
    mobileMenuBg?: string
  }
}

interface NavigationItem {
  id: string
  label: string
  path: string
}

function Header({ variant = 'default', customColors }: HeaderProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [isScrolled, setIsScrolled] = useState(false)

  const optionsItems: NavigationItem[] = [
    {
      id: 'calendario',
      label: 'Calendário',
      path: '/calendario',
    },
    {
      id: 'jornada',
      label: 'Jornada',
      path: '/jornada',
    },
    {
      id: 'sobre nos',
      label: 'Sobre nós',
      path: '/sobre-nos',
    },
    {
      id: 'nossos-valores',
      label: 'Nossos Valores',
      path: '/nossos-valores',
    },
    {
      id: 'contato',
      label: 'Contato',
      path: '/contato',
    },
  ]

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
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
    const handleScroll = () => {
      const scrollTop = window.scrollY
      setIsScrolled(scrollTop > 500)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleNavigation = (path: string) => {
    window.location.href = path
    setIsMobileMenuOpen(false)
  }

  const getColors = () => {
    if (variant === 'custom' && customColors) {
      return {
        headerBg: customColors.headerBg || 'var(--color-bah-purple)',
        searchIconMobile:
          customColors.searchIconMobile || 'var(--color-bah-green)',
        searchIconDesktop:
          customColors.searchIconDesktop || 'var(--color-bah-purple)',
        buttonHover: customColors.buttonHover || 'var(--color-bah-green)',
        mobileMenuBg: customColors.mobileMenuBg || 'var(--color-bah-purple)',
      }
    }

    return {
      headerBg: 'var(--color-bah-purple)',
      searchIconMobile: 'var(--color-bah-green)',
      searchIconDesktop: 'var(--color-bah-purple)',
      buttonHover: 'var(--color-bah-green)',
      mobileMenuBg: 'var(--color-bah-purple)',
    }
  }

  const SearchIcon = () => (
    <svg className="h-4 w-4 " fill="none" stroke="white" viewBox="0 0 24 24">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
      />
    </svg>
  )

  return (
    <>
      <header
        className={`fixed top-0 z-50 w-full h-20 transition-all duration-300 flex items-center justify-center ${
          isScrolled ? 'bg-white shadow-lg' : 'bg-white shadow-lg'
        } `}
        style={{
          backgroundColor: isScrolled ? getColors().headerBg : 'white',
        }}
      >
        <div className="w-full max-w-7xl mx-auto px-4 flex items-center justify-between">
          <div className="flex items-center relative w-20 h-16">
            <img
              src="/src/assets/bah-bg-white.png"
              alt="Logo"
              className={`h-14 w-auto transition-all duration-300 absolute top-1 left-0 ${
                isScrolled ? 'opacity-0 scale-95' : 'opacity-100 scale-100'
              }`}
            />
            <img
              src="/src/assets/bah-bg-purple.png"
              alt="Logo"
              className={`h-16 w-auto transition-all duration-200 absolute top-0 left-0 ${
                isScrolled ? 'opacity-100 scale-100' : 'opacity-0 scale-100'
              }`}
            />
          </div>

          {isScrolled && (
            <div className="flex-1 max-w-sm mx-4 md:mx-8 animate-in slide-in-from-top-2 duration-300">
              <form className="flex items-center w-45 md:w-full bg-white rounded-full overflow-hidden h-11 md:h-auto ml-10 md:ml-0">
                <Input
                  type="text"
                  placeholder="Conheça as iniciativas"
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="flex-1 px-2 md:px-6 py-3 text-xs md:text-sm text-black bg-transparent !border-0 !outline-none !ring-0 !shadow-none focus:!border-0 focus:!outline-none focus:!ring-0 focus:!shadow-none placeholder:text-black placeholder:font-weight-bold ml-2 md:ml-0"
                />
                <div
                  className="w-6 h-6 rounded-full flex items-center justify-center mx-2 cursor-pointer"
                  style={{
                    backgroundColor:
                      window.innerWidth < 768
                        ? getColors().searchIconMobile
                        : getColors().searchIconDesktop,
                  }}
                >
                  <SearchIcon />
                </div>
              </form>
            </div>
          )}

          {isScrolled && (
            <nav className="hidden md:flex items-center space-x-6">
              {optionsItems.map(item => (
                <button
                  key={item.id}
                  onClick={() => handleNavigation(item.path)}
                  className="px-3 py-2 text-sm font-medium text-white hover:underline cursor-pointer transition-all duration-300 ease-in-out hover:-translate-y-1"
                  style={{
                    color: 'white',
                  }}
                  onMouseEnter={e => {
                    e.currentTarget.style.color = getColors().buttonHover
                  }}
                  onMouseLeave={e => {
                    e.currentTarget.style.color = 'white'
                  }}
                >
                  {item.label}
                </button>
              ))}
            </nav>
          )}
        </div>
      </header>

      <button
        className="md:hidden fixed top-5 right-4 transition-colors z-50 bg-transparent p-2 rounded-full"
        style={{
          color: isScrolled
            ? getColors().buttonHover
            : 'var(--color-bah-purple)',
        }}
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M3 12h18" />
          <path d="M3 18h18" />
          <path d="M3 6h18" />
        </svg>
      </button>

      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-40 md:hidden backdrop-blur-sm">
          <div
            className="fixed right-0 top-0 h-full w-[70%] shadow-xl animate-in slide-in-from-right duration-300"
            style={{
              backgroundColor: getColors().mobileMenuBg,
            }}
          >
            <div className="flex flex-col h-full">
              <div className="flex items-center justify-between p-6 border-b border-white/20">
                <h2 className="text-xl font-semibold text-white">Menu</h2>
                <button
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="text-white transition-colors"
                  onMouseEnter={e => {
                    e.currentTarget.style.color = getColors().buttonHover
                  }}
                  onMouseLeave={e => {
                    e.currentTarget.style.color = 'white'
                  }}
                >
                  <svg
                    className="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>

              <nav className="flex-1 p-6">
                <ul className="space-y-4">
                  {optionsItems.map(item => (
                    <li key={item.id}>
                      <button
                        onClick={() => handleNavigation(item.path)}
                        className="w-full text-left px-4 py-4 text-white hover:bg-white/10 rounded-lg transition-all duration-200 text-lg font-medium"
                        onMouseEnter={e => {
                          e.currentTarget.style.color = getColors().buttonHover
                        }}
                        onMouseLeave={e => {
                          e.currentTarget.style.color = 'white'
                        }}
                      >
                        {item.label}
                      </button>
                    </li>
                  ))}
                </ul>
              </nav>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default Header
