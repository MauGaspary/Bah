'use client'

import { Search, X } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Input } from '@/components/ui/Searchbar/Searchbar'
import SearchItem from '@/components/ui/Searchbar/SearchItem'
import { cn } from '@/lib/utils'

const mockIniciativas = [
  {
    id: '1',
    imageUrl: 'https://placehold.co/100x100',
    title: 'Recicla Mais',
    description: 'Projeto de reciclagem comunitária',
  },
  {
    id: '2',
    imageUrl: 'https://placehold.co/100x100',
    title: 'Energia Solar Popular',
    description: 'Iniciativa para casas com energia limpa',
  },
  {
    id: '3',
    imageUrl: 'https://placehold.co/100x100',
    title: 'Horta Urbana',
    description: 'Cultivo colaborativo em espaços públicos',
  },
  {
    id: '4',
    imageUrl: 'https://placehold.co/100x100',
    title: 'Reflorestamento Local',
    description: 'Plantio de árvores nativas na região',
  },
  {
    id: '5',
    imageUrl: 'https://placehold.co/100x100',
    title: 'Mobilidade Sustentável',
    description: 'Incentivo ao uso de bicicletas e transporte público',
  },
]

function SearchDropdown() {
  const [searchQuery, setSearchQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')
  const [isOpen, setIsOpen] = useState(false)
  const [isFullscreen, setIsFullscreen] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)
  const navigate = useNavigate()

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedQuery(searchQuery), 1000)
    return () => clearTimeout(timer)
  }, [searchQuery])

  const filteredResults = debouncedQuery.trim()
    ? mockIniciativas.filter(
        item =>
          item.title.toLowerCase().includes(debouncedQuery.toLowerCase()) ||
          item.description.toLowerCase().includes(debouncedQuery.toLowerCase())
      )
    : []

  useEffect(() => {
    function handleClickOutside(event: Event) {
      const mouseEvent = event as MouseEvent
      if (
        containerRef.current &&
        !containerRef.current.contains(mouseEvent.target as Node)
      ) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  useEffect(() => {
    setIsOpen(filteredResults.length > 0)
  }, [filteredResults.length])

  const handleSelectItem = (item: (typeof mockIniciativas)[0]) => {
    setIsOpen(false)
    setIsFullscreen(false)
    navigate(`/iniciativa/${item.id}`)
  }

  const handleSearchClick = () => {
    if (searchQuery.trim()) {
      navigate(`/results?q=${encodeURIComponent(searchQuery)}`)
      setIsFullscreen(false)
    }
  }

  const handleFocus = () => {
    if (window.innerWidth < 640) {
      setIsFullscreen(true)
    } else {
      setIsOpen(filteredResults.length > 0)
    }
  }

  return (
    <>
      <div ref={containerRef} className="relative w-full max-w-2xl">
        <form
          className={cn(
            'flex items-center w-full bg-white overflow-hidden h-12 shadow-lg',
            isOpen ? 'rounded-t-3xl' : 'rounded-full'
          )}
        >
          <Input
            type="text"
            placeholder="Conheça as iniciativas"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            onFocus={handleFocus}
            className="flex-1 px-6 py-3 text-sm text-black bg-transparent !border-0 !outline-none !ring-0 focus-visible:!ring-0 placeholder:text-black placeholder:font-semibold"
          />
          <div
            onClick={handleSearchClick}
            className="w-8 h-8 rounded-full flex items-center justify-center mr-2 cursor-pointer bg-bah-purple hover:bg-bah-purple/90 transition-colors"
          >
            <Search className="h-4 w-4 text-white" />
          </div>
        </form>

        {!isFullscreen && isOpen && filteredResults.length > 0 && (
          <div
            className={cn(
              'absolute top-full left-0 right-0 bg-white rounded-b-3xl shadow-2xl',
              'border border-gray-200 max-h-[500px] overflow-y-auto z-50',
              'animate-in fade-in-0 slide-in-from-top-2 duration-200'
            )}
          >
            {filteredResults.map(item => (
              <div
                key={item.id}
                onClick={() => handleSelectItem(item)}
                className="cursor-pointer hover:bg-gray-50 transition-colors py-2"
              >
                <SearchItem {...item} />
              </div>
            ))}
          </div>
        )}
      </div>

      {isFullscreen && (
        <div className="fixed inset-0 z-50 bg-white flex flex-col animate-in fade-in duration-200">
          <div className="flex items-center gap-2 p-4 border-b border-gray-200">
            <button onClick={() => setIsFullscreen(false)}>
              <X className="w-6 h-6 text-gray-600" />
            </button>
            <Input
              autoFocus
              type="text"
              placeholder="Buscar iniciativas..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="flex-1 text-base px-3 py-2 border-0 focus:ring-0 focus-visible:ring-0 outline-none"
            />
            <Search
              onClick={handleSearchClick}
              className="w-5 h-5 text-gray-700 cursor-pointer"
            />
          </div>

          <div className="flex-1 overflow-y-auto p-2">
            {filteredResults.length === 0 && debouncedQuery.trim() ? (
              <p className="text-center text-gray-500 mt-6">
                Nenhum resultado encontrado
              </p>
            ) : (
              filteredResults.map(item => (
                <div
                  key={item.id}
                  onClick={() => handleSelectItem(item)}
                  className="cursor-pointer hover:bg-gray-50 transition-colors p-2 rounded-lg"
                >
                  <SearchItem {...item} />
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </>
  )
}
export default SearchDropdown;