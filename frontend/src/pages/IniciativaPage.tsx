import { useEffect, useState } from "react"
import { useParams , Link } from "react-router-dom"


import type { CarouselApi } from "@/components/ui/carousel"
import type { Iniciativa, IniciativaHorario } from "@/interfaces/IIniciativas";

import {
  Carousel,
  CarouselContent,
  CarouselItem,
} from "@/components/ui/carousel"
import Footer from "@/components/ui/Footer/Footer";
import Header from "@/components/ui/Header/Header"
import HorarioCard from "@/components/ui/HorarioCard"
import { getImageUrl } from "@/lib/imageUrl"
import { getIniciativaById } from "@/service/search";

function IniciativaPage() {
  const { id } = useParams<{ id: string }>()
  const [iniciativa, setIniciativa] = useState<Iniciativa | null>(null);
  const [activeIndex, setActiveIndex] = useState(0);
  const [carouselApi, setCarouselApi] = useState<CarouselApi | null>(null);

  type EmblaWithSelected = CarouselApi & {
    selectedScrollSnap?: () => number
  }

  useEffect(() => {
    if (!carouselApi) return

    const updateActive = () => {
      const sel = (carouselApi as EmblaWithSelected).selectedScrollSnap?.() ?? 0
      setActiveIndex(Number(sel))
    }

    updateActive()
    carouselApi.on?.("select", updateActive)
    carouselApi.on?.("reInit", updateActive)

    return () => {
      carouselApi.off?.("select", updateActive)
      carouselApi.off?.("reInit", updateActive)
    }
  }, [carouselApi])

  function scrollToIndex(i: number) {
    if (carouselApi?.scrollTo) {
      carouselApi.scrollTo(i)
      setActiveIndex(i)
    }
  }

  useEffect(() => {
    async function fetchIniciativa() {
      if (id) {
        try {
          const response = await getIniciativaById(id);
          setIniciativa(response);
        } catch {
          console.error("Error fetching iniciativa data:", new Error('fetch failed'));
          // navigate('/not-found'); 
        }
      }
    }

    fetchIniciativa()
  }, [id]);

  

  if(!iniciativa){
      return;
  }

  const processedHorarios = (iniciativa.horarios ?? []).map((horario) => {
    const h = horario as IniciativaHorario
    const date = h.data_evento ? new Date(`${h.data_evento}T00:00:00`) : null
    const weekdayNames = [
      'Domingo',
      'Segunda',
      'Terça',
      'Quarta',
      'Quinta',
      'Sexta',
      'Sábado',
    ]
    const dia = date ? weekdayNames[date.getDay()] : ''
    const data = date
      ? new Intl.DateTimeFormat('pt-BR', {
          day: '2-digit',
          month: 'long',
          year: 'numeric',
        }).format(date)
      : ''
    const modalidade = h.tipo
      ? String(h.tipo).charAt(0).toUpperCase() + String(h.tipo).slice(1)
      : ''

    return {
      ...h,
      dia,
      data,
      modalidade,
    }
  })

  return (
    <>
      <Header />

      <section
        className={
          'relative min-h-[280px] md:min-h-[360px] w-full bg-cover bg-top md:bg-center bg-no-repeat md:bg-fixed flex items-end'
        }
        aria-label="Hero da iniciativa"
      >
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/10 pointer-events-none">
          <img
            src={getImageUrl(iniciativa.imagem_url) || ''}
            alt={iniciativa.titulo}
            className="w-full h-full object-cover"
          />
        </div>

        <div className="w-full max-w-100vw mx-auto px-4 py-10 md:py-16">
          <div className="relative">
            <div className="absolute left-1/2 -translate-x-1/2 bottom-0 translate-y-4/3 md:translate-y-5/3 z-10">
              <Link to={iniciativa.link ?? '#'}>
                <button
                  className="bg-purple-600 text-white px-6 md:px-10 py-2 md:py-3 rounded-xl text-sm md:text-base shadow-md hover:bg-purple-700 transition cursor-pointer"
                  aria-label="Inscrever-se"
                >
                  <span className="text-xl">Inscrever-se</span>
                </button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      <main className="w-full max-w-6xl mx-auto px-4 py-10 md:py-16">
        <article className="prose prose-lg dark:prose-invert mx-auto text-center max-w-3xl">
          <h1 className="text-2xl md:text-4xl font-bold">
            {iniciativa.titulo}
          </h1>
          <p className="mt-2 text-base md:text-lg text-gray-700 dark:text-gray-300">
            {iniciativa.descricao}
          </p>
        </article>

        <section className="mt-10">
            <div className="flex justify-center items-center md:hidden">
            <Carousel className="w-full max-w-xs" setApi={setCarouselApi}>
              <CarouselContent>
                {processedHorarios.map((h, index) => (
                  <CarouselItem key={index}>
                    <div className="p-1">
                      <HorarioCard item={h} />
                    </div>
                  </CarouselItem>
                ))}
              </CarouselContent>
            </Carousel>
            </div>

          <div className={`hidden md:grid md:gap-6 flex justify-center items-center ${
            processedHorarios.length === 1 ? 'md:grid-cols-1 max-w-md mx-auto' :
            processedHorarios.length === 2 ? 'md:grid-cols-2 max-w-2xl mx-auto' :
            'md:grid-cols-3'
          }`}>
            {processedHorarios.map((h) => (
              <div key={h.id ?? Math.random().toString()} className="px-2">
                <HorarioCard item={h} />
              </div>
            ))}
          </div>

          {processedHorarios.length > 0  && (
             <div className="mt-4 flex justify-center gap-2 md:hidden">
            {Array.from({ length: processedHorarios.length }, (_, i) => i).map(i => {
              const key = processedHorarios[i]?.id ?? i
              const activeDot = Math.min(activeIndex, processedHorarios.length - 1)
              return (
                <span
                  key={key}
                  role="button"
                  aria-label={`Ir para card ${i + 1}`}
                  onClick={() => scrollToIndex(i)}
                  className={`h-2 w-2 rounded-full ${
                    i === activeDot ? 'bg-[#6B4BA9]' : 'bg-gray-300'
                  } cursor-pointer`}
                />
              )
            })}
          </div>
          )}
        </section>
      </main>

      <Footer />
    </>
  )
}

export default IniciativaPage
