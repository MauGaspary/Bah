import { useState, useEffect } from 'react'
import * as React from 'react'

interface HeaderProps {
  variant?: 'default' | 'secondary' | string
  withSearchBar?: boolean
  hasBackButton?: boolean
  className?: string
  logo?: string
  onBack?: () => void
  onSearch?: (query: string) => void
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

const CloseIcon = () => (
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
      d="M6 18L18 6M6 6l12 12"
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

const ArrowLeftIcon = () => (
  <svg
    className="h-5 w-5"
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M15 19l-7-7 7-7"
    />
  </svg>
)

function Header({
  variant = 'default',
  withSearchBar = false,
  hasBackButton = false,
  className = '',
  logo = '/src/assets/logo.png',
  onBack,
  onSearch,
}: HeaderProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

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

  const handleNavigation = (path: string) => {
    window.location.href = path
    setIsMobileMenuOpen(false)
  }

  const handleBackClick = () => {
    if (onBack) {
      onBack()
    } else {
      window.history.back()
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (onSearch) {
      onSearch(searchQuery)
    }
  }

  const getVariantStyles = () => {
    if (variant === 'default') {
      return 'bg-gradient-to-r from-purple-800 to-purple-900 text-white'
    }
    return 'bg-white text-gray-900 shadow-sm'
  }

  const getMenuButtonStyles = () => {
    if (variant === 'default') {
      return 'text-white hover:bg-white hover:bg-opacity-10'
    }
    return 'text-gray-700 hover:bg-gray-100'
  }

  return (
    <header
      className={`sticky top-0 z-50 w-full ${getVariantStyles()} ${className}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Left side - Back button and Logo */}
          <div className="flex items-center space-x-4">
            {hasBackButton && (
              <button
                onClick={handleBackClick}
                className={`p-2 rounded-md transition-colors ${getMenuButtonStyles()}`}
                aria-label="Voltar"
              >
                <ArrowLeftIcon />
              </button>
            )}

            <div className="flex-shrink-0">
              <img src={logo} alt="Logo" className="h-8 w-auto" />
            </div>
          </div>

          {/* Center - Search Bar (Desktop) */}
          {withSearchBar && (
            <div className="hidden md:flex flex-1 max-w-md mx-8">
              <form onSubmit={handleSearch} className="relative w-full">
                <input
                  type="text"
                  placeholder="Buscar..."
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="w-full px-4 py-2 pl-10 pr-4 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <SearchIcon />
              </form>
            </div>
          )}

          {/* Right side - Navigation and Menu */}
          <div className="flex items-center space-x-4">
            <nav className="hidden md:flex space-x-8">
              {optionsItems.map(item => (
                <button
                  key={item.id}
                  onClick={() => handleNavigation(item.path)}
                  className="px-4 py-2 text-sm font-medium  transition-colors"
                >
                  {item.label}
                </button>
              ))}
            </nav>

            <div className="md:hidden">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className={`p-2 rounded-md transition-colors ${getMenuButtonStyles()}`}
              >
                {isMobileMenuOpen ? <CloseIcon /> : <MenuIcon />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Search Bar */}
        {withSearchBar && (
          <div className="md:hidden pb-4">
            <form onSubmit={handleSearch} className="relative">
              <input
                type="text"
                placeholder="Buscar..."
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

      {isMobileMenuOpen && (
        <div className="md:hidden">
          <div
            className={`px-2 pt-2 pb-3 space-y-1 border-t ${
              variant === 'secondary'
                ? 'bg-purple-800 border-purple-700'
                : 'bg-white border-gray-200'
            }`}
          >
            {optionsItems.map(item => (
              <button
                key={item.id}
                onClick={() => handleNavigation(item.path)}
                className={`block w-full text-left px-3 py-2 text-base font-medium rounded-md transition-colors ${
                  variant === 'secondary'
                    ? 'text-white hover:bg-purple-700'
                    : 'text-gray-900 hover:bg-gray-100'
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </header>
  )
}

export default Header
