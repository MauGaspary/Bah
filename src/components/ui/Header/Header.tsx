import { Menu, X } from 'lucide-react'
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

import { Input } from '../Searchbar/Searchbar'

import { optionsItems } from './NavigationsItens'
import type { NavigationItem } from './NavigationsItens'

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

function Header({ variant = 'default', customColors }: HeaderProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [isScrolled, setIsScrolled] = useState(false)
  const [isSearchIconHovered, setIsSearchIconHovered] = useState(false)

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

  const handleNavigation = (item: NavigationItem) => {
    const mapIdToSection: Record<string, string> = {
      calendario: 'calendar-section',
      jornada: 'journey-section',
      'sobre nos': 'about-section',
      'nossos-valores': 'values-section',
      contato: 'contact-section',
    }

    let sectionId = mapIdToSection[item.id]
    if (item.id === 'calendario' && typeof window !== 'undefined') {
      sectionId =
        window.innerWidth < 768 ? 'calendar-section-mobile' : 'calendar-section'
    }

    if (sectionId) {
      const scrollToSection = () => {
        const el = document.getElementById(sectionId)
        if (el) {
          el.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
      }

      if (window.location.pathname !== '/') {
        navigate('/', { state: { scrollTo: sectionId } })
      } else {
        scrollToSection()
      }

      setIsMobileMenuOpen(false)
      return
    }

    navigate(item.path)
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

  const handleHeaderSearch = () => {
    if (searchQuery.trim()) {
      navigate(`/results?q=${encodeURIComponent(searchQuery)}`)
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
          <div
            className="flex items-center relative w-20 h-16 cursor-pointer"
            onClick={() => {
              const sectionId = 'home-section'
              const scrollToSection = () => {
                const el = document.getElementById(sectionId)
                if (el) {
                  el.scrollIntoView({ behavior: 'smooth', block: 'start' })
                }
              }

              if (window.location.pathname !== '/') {
                navigate('/', { state: { scrollTo: sectionId } })
              } else {
                scrollToSection()
              }
              setIsMobileMenuOpen(false)
            }}
            aria-label="Ir para início"
            role="button"
          >
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
              className={`h-14 w-auto transition-all duration-200 absolute top-1 left-0 ${
                isScrolled ? 'opacity-100 scale-100' : 'opacity-0 scale-100'
              }`}
            />
          </div>

          {isScrolled && (
            <div className="flex-1 max-w-sm mx-4 md:mx-20 lg:mx-8 animate-in slide-in-from-top-2 duration-300">
              <form
                onSubmit={e => {
                  e.preventDefault()
                  handleHeaderSearch()
                }}
                className="flex items-center w-45 md:w-full bg-white rounded-full overflow-hidden h-11 md:h-auto ml-4 md:ml-4 lg:ml-0 max-[500px]:max-w-[250px] max-[500px]:ml-6"
              >
                <Input
                  type="text"
                  placeholder="Conheça as iniciativas"
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="flex-1 px-2 md:px-6 py-3 text-xs md:text-sm text-black bg-transparent !border-0 !outline-none !ring-0 !shadow-none focus:!border-0 focus:!outline-none focus:!ring-0 focus:!shadow-none placeholder:text-black placeholder:font-weight-bold ml-2 md:ml-0 max-[500px]:placeholder:text-xs truncate placeholder:truncate"
                />
                <button
                  type="submit"
                  onClick={handleHeaderSearch}
                  className="w-6 h-6 rounded-full flex items-center justify-center mx-2 cursor-pointer transition-all duration-300"
                  style={{
                    backgroundColor:
                      window.innerWidth < 1024
                        ? getColors().searchIconMobile
                        : getColors().searchIconDesktop,
                    transform: isSearchIconHovered
                      ? 'scale(110%)'
                      : 'scale(100%)',
                    boxShadow: isSearchIconHovered
                      ? '0 4px 12px rgba(0,0,0,0.15)'
                      : 'none',
                  }}
                  onMouseEnter={() => setIsSearchIconHovered(true)}
                  onMouseLeave={() => setIsSearchIconHovered(false)}
                  aria-label="Buscar"
                >
                  <SearchIcon />
                </button>
              </form>
            </div>
          )}

          {isScrolled && (
            <nav className="hidden lg:flex items-center space-x-6">
              {optionsItems.map(item => (
                <button
                  key={item.id}
                  onClick={() => handleNavigation(item)}
                  className="px-3 py-2 text-sm font-medium text-white hover:text-bah-green cursor-pointer transition-all duration-300 ease-in-out hover:-translate-y-1 font-mulish"
                >
                  {item.label}
                </button>
              ))}
            </nav>
          )}
        </div>
      </header>

      <button
        className="lg:hidden fixed top-5 right-4 transition-colors z-50 bg-transparent p-2 rounded-full"
        style={{
          color: isScrolled
            ? getColors().buttonHover
            : 'var(--color-bah-purple)',
        }}
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      >
        {!isMobileMenuOpen ? <Menu size={26} /> : <X size={26} />}
      </button>

      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-40 lg:hidden backdrop-blur-sm">
          <div
            className="fixed right-0 top-0 h-full w-[70%] shadow-xl animate-in slide-in-from-right duration-300"
            style={{
              backgroundColor: getColors().mobileMenuBg,
            }}
          >
            <div className="flex flex-col h-full">
              <div className="flex items-center justify-center p-6 border-b border-white/20">
                <h2 className="text-xl font-semibold text-white">Menu</h2>
              </div>

              <nav className="flex-1 p-6">
                <ul className="space-y-4">
                  {optionsItems.map(item => (
                    <li key={item.id}>
                      <button
                        onClick={() => handleNavigation(item)}
                        className="w-full text-left px-4 py-4 text-white hover:bg-white/10 hover:text-bah-green rounded-lg transition-all duration-200 text-lg font-medium font-mulish"
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
