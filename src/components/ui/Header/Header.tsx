import { useState, useEffect } from 'react'
import * as React from 'react'
import { Input } from '../Searchbar/Searchbar'

interface HeaderProps {
  variant?: 'default' | 'secondary'
  withSearchBar?: boolean
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
  <svg
    className="h-4 w-4"
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
    />
  </svg>
)

function Header({ variant = 'default', withSearchBar = false }: HeaderProps) {
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
      id: 'sobre nos',
      label: 'Sobre nós',
      path: '/sobre-nos',
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
      className={`fixed top-0 z-50 w-full transition-all duration-300 ${
        isScrolled ? 'bg-bah-purple' : 'bg-white shadow-lg'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Left side - Logo */}
          <div className="flex items-center justify space-x-4 relative w-20 h-16 mt-4">
            {/* Logo branca (estado inicial) */}
            <img
              src="/src/assets/bah-bg-white.png"
              alt="Logo"
              className={`h-12 w-auto transition-all duration-300 absolute top-0 left-0 ${
                isScrolled ? 'opacity-0 scale-95' : 'opacity-100 scale-100'
              }`}
            />
            {/* Logo roxa (estado após scroll) */}
            <img
              src="/src/assets/bah-bg-purple.png"
              alt="Logo"
              className={`h-12 w-auto transition-all duration-200 absolute top-0 left-0 ${
                isScrolled ? 'opacity-100 scale-100' : 'opacity-0 scale-100'
              }`}
            />
          </div>

          {/* Center - Search Bar (Desktop) */}
          {withSearchBar && (
            <div className="hidden md:flex flex-1 max-w-md mx-8">
              <form className="relative w-full">
                <Input
                  type="text"
                  placeholder="Pesquisar iniciativas"
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="w-full px-4 py-2 pl-10 pr-4 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <SearchIcon />
              </form>
            </div>
          )}
        </div>

        {/* Mobile Search Bar */}
        {withSearchBar && isScrolled && (
          <div className="md:hidden pb-4 animate-in slide-in-from-top-2 duration-300">
            <form className="relative">
              <Input
                type="text"
                placeholder="Pesquisar iniciativas"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="w-full px-4 py-2 pl-10 pr-4 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <div className="absolute left-3 top-2.5 text-gray-400">
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
