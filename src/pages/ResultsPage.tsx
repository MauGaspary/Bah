import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'

import type { Iniciativa } from '@/interfaces/IIniciativas'

import CardItem from '@/components/ui/CardItem'
import Header from '@/components/ui/Header/Header'
import { searchIniciativas } from '@/service/search'

function ResultsPage() {
  const [searchParams] = useSearchParams()
  const [results, setResults] = useState<Iniciativa[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [total, setTotal] = useState(0)
  const query = searchParams.get('q') || ''

  useEffect(() => {
    async function fetchResults() {
      setIsLoading(true)
      try {
        const response = await searchIniciativas({
          q: query,
          size: 20,
        })
        setResults(response.items)
        setTotal(response.total)
      } catch (error) {
        console.error('Erro ao buscar resultados:', error)
        setResults([])
        setTotal(0)
      } finally {
        setIsLoading(false)
      }
    }

    fetchResults()
  }, [query])

  return (
    <div>
      <Header variant="default" />
      <main className="min-h-screen bg-white py-8">
        <div className="container mx-auto px-4 max-w-4xl">
          <div className="pt-20">
            <h1 className="text-2xl font-bold mb-2">
              Resultados para: "{query}"
            </h1>
            <p className="text-label-secondary mb-6">
              {total}{' '}
              {total === 1 ? 'resultado encontrado' : 'resultados encontrados'}
            </p>

            {isLoading ? (
              <div className="text-center py-8">Carregando...</div>
            ) : results.length === 0 ? (
              <div className="text-center py-8 text-label-secondary">
                Nenhum resultado encontrado
              </div>
            ) : (
              <div className="flex flex-col gap-8">
                {results.map(iniciativa => (
                  <CardItem
                    key={iniciativa.id}
                    id={iniciativa.id}
                    imageUrl={iniciativa.imagem_url}
                    title={iniciativa.titulo}
                    description={iniciativa.descricao}
                    horarios={iniciativa.horarios}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default ResultsPage
