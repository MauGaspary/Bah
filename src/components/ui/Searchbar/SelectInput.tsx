'use client'

import { Search } from 'lucide-react'
import { useEffect, useRef, useState } from "react"
import { useNavigate } from "react-router-dom"

import SearchItem from "@/components/ui/Searchbar/SearchItem"
import { Input } from "@/components/ui/Searchbar/Searchbar"
import { cn } from "@/lib/utils"

const mockIniciativas = [
  {
    id: "1",
    imageUrl: "https://placehold.co/100x100",
    title: "Recicla Mais",
    description: "Projeto de reciclagem comunitária",
  },
  {
    id: "2",
    imageUrl: "https://placehold.co/100x100",
    title: "Energia Solar Popular",
    description: "Iniciativa para casas com energia limpa",
  },
  {
    id: "3",
    imageUrl: "https://placehold.co/100x100",
    title: "Horta Urbana",
    description: "Cultivo colaborativo em espaços públicos",
  },
  {
    id: "4",
    imageUrl: "https://placehold.co/100x100",
    title: "Reflorestamento Local",
    description: "Plantio de árvores nativas na região",
  },
  {
    id: "5",
    imageUrl: "https://placehold.co/100x100",
    title: "Mobilidade Sustentável",
    description: "Incentivo ao uso de bicicletas e transporte público",
  },
]

export function SelectInput() {
  const [searchQuery, setSearchQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')
  const [isOpen, setIsOpen] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)
  const navigate = useNavigate()

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(searchQuery)
    }, 1000)
    return () => clearTimeout(timer)
  }, [searchQuery])

  const filteredResults = debouncedQuery.trim() 
    ? mockIniciativas.filter(item => 
        item.title.toLowerCase().includes(debouncedQuery.toLowerCase()) ||
        item.description.toLowerCase().includes(debouncedQuery.toLowerCase())
      )
    : []

  useEffect(() => {
    function handleClickOutside(event: Event) {
      const mouseEvent = event as MouseEvent
      if (containerRef.current && !containerRef.current.contains(mouseEvent.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  useEffect(() => {
    setIsOpen(filteredResults.length > 0)
  }, [filteredResults.length])

  const handleSelectItem = (item: typeof mockIniciativas[0]) => {
    setIsOpen(false)
    navigate(`/iniciativa/${item.id}`)
  }

  const handleSearchClick = () => {
    if (searchQuery.trim()) {
      navigate(`/results?q=${encodeURIComponent(searchQuery)}`)
    }
  }

  return (
    <div ref={containerRef} className="relative w-full max-w-2xl">
      <form className="flex items-center w-full bg-white rounded-full overflow-hidden h-12 shadow-lg">
        <Input
          type="text"
          placeholder="Conheça as iniciativas"
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          onFocus={() => filteredResults.length > 0 && setIsOpen(true)}
          className="flex-1 px-6 py-3 text-sm text-black bg-transparent !border-0 !outline-none !ring-0 !shadow-none focus:!border-0 focus:!outline-none focus:!ring-0 focus:!shadow-none placeholder:text-black placeholder:font-semibold"
        />
        <div 
          onClick={handleSearchClick}
          className="w-8 h-8 rounded-full flex items-center justify-center mr-2 cursor-pointer bg-bah-purple hover:bg-bah-purple/90 transition-colors"
        >
          <Search className="h-4 w-4 text-white" />
        </div>
      </form>

      {isOpen && filteredResults.length > 0 && (
        <div 
          className={cn(
            "absolute top-full left-0 right-0 mt-2 bg-white rounded-lg shadow-2xl",
            "border border-gray-200 max-h-[500px] overflow-y-auto z-50",
            "animate-in fade-in-0 slide-in-from-top-2 duration-200"
          )}
        >
          {filteredResults.map((item) => (
            <div
              key={item.id}
              onClick={() => handleSelectItem(item)}
              className="cursor-pointer hover:bg-gray-50 transition-colors py-2 first:rounded-t-lg last:rounded-b-lg"
            >
              <SearchItem
                imageUrl={item.imageUrl}
                title={item.title}
                description={item.description}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
