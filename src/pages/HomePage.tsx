import SearchDropdown from '@/components/ui/Searchbar/SearchDropdown'
import { useEffect, useMemo, useState } from 'react'
import { useLocation } from 'react-router-dom'
import Header from '@/components/ui/Header/Header'
import CalendarSection from '@/components/ui/CalendarSection/CalendarSection'
import type { CalendarEvent } from '@/components/ui/CalendarSection/CalendarSection'
import UpcomingCarousel from '@/components/ui/UpcomingCarousel/UpcomingCarousel'
import { fetchCalendarioMensal } from '@/service/calendario'
import { ChevronDown } from 'lucide-react'

function HomePage() {
  const location = useLocation()
  const tags = [
    { name: 'Aceleração', value: 'aceleracao' },
    { name: 'Projetos', value: 'projetos' },
    { name: 'Investidores', value: 'investidores' },
    { name: 'Coworking', value: 'coworking' },
    { name: 'Mentorias', value: 'mentorias' },
  ]

  useEffect(() => {
    const state = location.state as { scrollTo?: string } | null
    if (state?.scrollTo) {
      // limpa o estado para evitar scroll repetido
      history.replaceState({}, '')
      const el = document.getElementById(state.scrollTo)
      if (el) {
        setTimeout(() => {
          el.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }, 50)
      }
    }
  }, [location.state])
  const [eventsAll, setEventsAll] = useState<CalendarEvent[]>([])

  useEffect(() => {
    const todayIso = new Date().toISOString().slice(0, 10)
    fetchCalendarioMensal(todayIso)
      .then(resp => {
        const inferCategory = (names: string[]): CalendarEvent['category'] => {
          const n = names.map(s => s.toLowerCase())
          if (n.some(s => s.includes('hack'))) return 'hackathon'
          if (n.some(s => s.includes('work'))) return 'workshop'
          if (n.some(s => s.includes('feira'))) return 'feira'
          if (n.some(s => s.includes('meet'))) return 'meetup'
          if (n.some(s => s.includes('network'))) return 'networking'
          return 'meetup'
        }

        const mapped: CalendarEvent[] = resp.dias.flatMap(dia =>
          dia.iniciativas.map(item => ({
            id: item.horario_id,
            title: item.titulo,
            description: item.descricao,
            date: dia.data,
            category: inferCategory(item.tags.map(t => t.nome)),
            location: item.local,
            imageUrl: undefined,
            featured: item.destaque,
          }))
        )
        setEventsAll(mapped)
      })
      .catch(() => {
        setEventsAll([])
      })
  }, [])
  const eventsNext15Days = useMemo(() => {
    const todayIso = new Date().toISOString().slice(0, 10)
    const end = new Date()
    end.setDate(end.getDate() + 15)
    const endIso = end.toISOString().slice(0, 10)
    return eventsAll.filter(e => e.date >= todayIso && e.date <= endIso)
  }, [eventsAll])
  return (
    <>
      <Header variant="default" />
      <main
        className="min-h-screen h-full overflow-x-hidden bg-[url('../src/assets/background.png')] bg-cover bg-top md:bg-center  bg-no-repeat md:bg-fixed w-full flex items-center justify-center relative"
        id="home-section"
      >
        <section className="container mx-auto px-4 py-8 md:py-20">
          <img
            src="../src/assets/logo.png"
            alt="logo"
            className="w-32 md:w-40 h-24 md:h-30 mb-3 mx-auto hidden md:block"
          />
          <div className="flex items-center justify-center w-full max-w-[28rem] mx-auto">
            <h1 className="text-white text-5xl md:text-4xl text-center mb-6 md:mb-4 font-mulish max-w-4xl mx-auto px-4">
              Conecte-se à <span className="font-bold italic">inovação</span> em
              Caxias do Sul
            </h1>
          </div>

          <p className="md:hidden text-white text-2xl font-mulish font-normal text-center mb-12 max-w-sm mx-auto px-4">
            Explore cursos, eventos e desafios de inovação que podem impulsionar
            sua jornada
          </p>
          <div className="flex justify-center max-w-3xl mx-auto mb-8 md:mb-4 px-4">
            <SearchDropdown />
          </div>

          <div className="flex flex-wrap justify-center gap-2 md:gap-3 px-4">
            {tags.map(tag => (
              <button
                key={tag.value}
                className="bg-bah-purple/60 hover:bg-bah-purple/80 cursor-pointer text-white px-3 py-1.5 rounded-full text-sm font-medium border border-bah-purple/30 transition-all duration-200"
              >
                {tag.name}
              </button>
            ))}
          </div>
          {/* Botão para descer até o calendário/carrossel — movido para fora da section */}
        </section>
        <div className="absolute left-1/2 -translate-x-1/2 bottom-4 md:bottom-6">
          <button
            type="button"
            aria-label="Ir para o calendário"
            onClick={() => {
              const targetId =
                window.innerWidth < 768
                  ? 'calendar-section-mobile'
                  : 'calendar-section'
              const el = document.getElementById(targetId)
              if (el) {
                el.scrollIntoView({ behavior: 'smooth', block: 'start' })
              }
            }}
            className="rounded-full p-2 text-white/90 hover:text-white transition-colors animate-bounce"
          >
            <ChevronDown className="h-8 w-8" />
          </button>
        </div>
      </main>

      {/* Mobile: Carrossel de próximos eventos */}
      <div className="md:hidden" id="calendar-section-mobile">
        <UpcomingCarousel events={eventsNext15Days} />
      </div>

      {/* Desktop: Calendário com destaques */}
      <div className="hidden md:block" id="calendar-section">
        <CalendarSection events={eventsAll} />
      </div>

      {/* Jornada */}
      <section id="journey-section" className="container mx-auto px-4 py-16">
        <h2 className="text-3xl md:text-4xl font-bold text-center">Jornada</h2>
      </section>

      {/* Sobre nós */}
      <section id="about-section" className="container mx-auto px-4 py-16">
        <h2 className="text-3xl md:text-4xl font-bold text-center">
          Sobre nós
        </h2>
      </section>

      {/* Nossos Valores */}
      <section id="values-section" className="container mx-auto px-4 py-16">
        <h2 className="text-3xl md:text-4xl font-bold text-center">
          Nossos Valores
        </h2>
      </section>

      {/* Contato */}
      <section id="contact-section" className="container mx-auto px-4 py-16">
        <h2 className="text-3xl md:text-4xl font-bold text-center">Contato</h2>
      </section>
    </>
  )
}

export default HomePage
