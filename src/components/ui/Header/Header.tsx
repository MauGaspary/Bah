import { useState, useEffect } from 'react'
import * as React from 'react'
import { Input } from '../Searchbar/Searchbar'

interface HeaderProps {
  variant?: 'default' | 'secondary'
  logo?: string
}

interface NavigationItem {
  id: string
  label: string
  path: string
}

// Componentes de ícones simples
const MenuIcon = () => (
  <svg
    className="h-6 w-6"
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M4 6h16M4 12h16M4 18h16"
    />
  </svg>
)

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

function Header({ variant = 'default' }: HeaderProps) {
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
      setIsMobileMenuOpen(window.innerWidth < 768)
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY
      setIsScrolled(scrollTop > 50)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleNavigation = (path: string) => {
    window.location.href = path
    setIsMobileMenuOpen(false)
  }

  const getVariantStyles = () => {
    if (variant === 'default') {
      return 'bg-bah-purple'
    }
    return 'bg-white'
  }

  return (
    <header
      className={`fixed top-0 z-50 w-full h-20 transition-all duration-300 flex items-center justify-center ${
        isScrolled ? 'bg-bah-purple' : 'bg-white shadow-lg'
      }`}
    >
      <div className="w-full max-w-7xl mx-auto px-4 flex items-center justify-between">
        {/* Logo (esquerda) */}
        <div className="flex items-center relative w-20 h-16">
          {/* Logo branca (estado inicial) */}
          <img
            src="/src/assets/bah-bg-white.png"
            alt="Logo"
            className={`h-14 w-auto transition-all duration-300 absolute top-1 left-0 ${
              isScrolled ? 'opacity-0 scale-95' : 'opacity-100 scale-100'
            }`}
          />
          {/* Logo roxa (estado após scroll) */}
          <img
            src="/src/assets/bah-bg-purple.png"
            alt="Logo"
            className={`h-16 w-auto transition-all duration-200 absolute top-0 left-0 ${
              isScrolled ? 'opacity-100 scale-100' : 'opacity-0 scale-100'
            }`}
          />
        </div>

        {/* Search Bar (centro) - Só aparece após scroll */}
        {isScrolled && (
          <div className="flex-1 max-w-sm mx-8 animate-in slide-in-from-top-2 duration-300">
            <form className="flex items-center w-full bg-white rounded-full overflow-hidden">
              <Input
                type="text"
                placeholder="Conheça as iniciativas"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="flex-1 px-6 py-3 text-sm text-black bg-transparent !border-0 !outline-none !ring-0 !shadow-none focus:!border-0 focus:!outline-none focus:!ring-0 focus:!shadow-none"
              />
              <div className="bg-bah-purple w-6 h-6 rounded-full flex items-center justify-center mx-2">
                <SearchIcon />
              </div>
            </form>
          </div>
        )}

        {/* Navigation Buttons (direita) */}
        <nav className="hidden md:flex items-center space-x-6">
          {optionsItems.map(item => (
            <button
              key={item.id}
              onClick={() => handleNavigation(item.path)}
              className="px-3 py-2 text-sm font-medium text-white hover:text-green-400 hover:underline cursor-pointer transition-colors"
            >
              {item.label}
            </button>
          ))}
        </nav>

        {/* Mobile Search Bar - Só aparece após scroll */}
        {isScrolled && (
          <div className="md:hidden pb-4 animate-in slide-in-from-top-2 duration-300">
            <form className="flex items-center w-2/4 bg-white rounded-full overflow-hidden">
              <Input
                type="text"
                placeholder="Pesquisar iniciativas"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="flex-1 px-6 py-6 text-sm text-black bg-transparent !border-0 !outline-none !ring-0 !shadow-none focus:!border-0 focus:!outline-none focus:!ring-0 focus:!shadow-none placeholder:text-black placeholder:font-weight-bold"
              />
              <div className="bg-bah-purple w-8 h-8 rounded-full flex items-center justify-center mr-2">
                <SearchIcon />
              </div>
            </form>
          </div>
        )}
      </div>
    </header>
  )
}

export default Header
