import { Search } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { useLocation } from 'react-router-dom'

import Header from '@/components/ui/Header/Header'
import CalendarSection from '@/components/ui/CalendarSection/CalendarSection'
import UpcomingCarousel from '@/components/ui/UpcomingCarousel/UpcomingCarousel'
import { buildCalendarEvents } from '@/data/iniciativas'
import { Input } from '@/components/ui/Searchbar/Searchbar'

function HomePage() {
  const [searchQuery, setSearchQuery] = useState('')
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
  const eventsAll = useMemo(() => buildCalendarEvents(), [])
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
        className="min-h-screen h-full overflow-x-hidden bg-[url('../src/assets/background.png')] bg-cover bg-top md:bg-center  bg-no-repeat md:bg-fixed w-full flex items-center justify-center"
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
              Conecte-se à{' '}
              <span className="font-bold italic md:not-italic md:font-normal">
                inovação
              </span>{' '}
              em Caxias do Sul
            </h1>
          </div>

          <p className="md:hidden text-white text-2xl font-mulish font-normal text-center mb-12 max-w-sm mx-auto px-4">
            Explore cursos, eventos e desafios de inovação que podem impulsionar
            sua jornada
          </p>
          <div className="flex justify-center max-w-3xl mx-auto mb-8 md:mb-4 px-4">
            <form className="flex items-center w-full max-w-2xl bg-white rounded-full overflow-hidden h-12 shadow-lg">
              <Input
                type="text"
                placeholder="Conheça as iniciativas"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="flex-1 px-6 py-3 text-sm text-black bg-transparent !border-0 !outline-none !ring-0 !shadow-none focus:!border-0 focus:!outline-none focus:!ring-0 focus:!shadow-none placeholder:text-black placeholder:font-semibold"
              />
              <div className="w-8 h-8 rounded-full flex items-center justify-center mr-2 cursor-pointer bg-bah-purple">
                <Search className="h-4 w-4 text-white" />
              </div>
            </form>
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
        </section>
      </main>

      {/* Mobile: Carrossel de próximos eventos */}
      <div className="md:hidden">
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
        <h2 className="text-3xl md:text-4xl font-bold text-center">Sobre nós</h2>
      </section>

      {/* Nossos Valores */}
      <section id="values-section" className="container mx-auto px-4 py-16">
        <h2 className="text-3xl md:text-4xl font-bold text-center">Nossos Valores</h2>
      </section>

      {/* Contato */}
      <section id="contact-section" className="container mx-auto px-4 py-16">
        <h2 className="text-3xl md:text-4xl font-bold text-center">Contato</h2>
      </section>
    </>
  )
}

export default HomePage
