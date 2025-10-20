import { Calendar1, MapPinned, CalendarDays, Clock9 } from "lucide-react"

import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"
import Header from "@/components/ui/Header/Header"

const horarios = [
  {
    id: "seg",
    dia: "Segunda",
    modalidade: "Presencial",
    data: "18 de agosto 2025",
    horario: "13:00 - 18:00",
  },
  {
    id: "qua",
    dia: "Quarta",
    modalidade: "Online",
    data: "20 de agosto 2025",
    horario: "09:00 - 12:00",
  },
  {
    id: "sex",
    dia: "Sexta",
    modalidade: "Presencial",
    data: "22 de agosto 2025",
    horario: "14:00 - 18:00",
  },
]

function HorarioCard({ item }: { item: typeof horarios[number] }) {
  return (
    <div className="w-full max-w justify-center items-center md:max-w-sm mx-auto">
      <div className="h-full flex items-center justify-center border border-purple-200 rounded-xl bg-white dark:bg-gray-800 py-3 flex flex-col items-start gap-5 shadow-sm">
        <div className="flex flex-col w-full justify-center items-center gap-2">
          <div className="w-6 h-6 rounded-md bg-purple-100 flex items-center justify-center text-bah-purple">
            <Calendar1 />
          </div>
          <h3 className="text-2xl font-semibold dark:text-white">{item.dia}</h3>
        </div>

        <div className="flex w-full justify-center items-center gap-3">
            <MapPinned className="w-6 h-6 text-bah-purple"/>
            <div className="text-sm text-gray-600 dark:text-gray-300"> 
                {item.modalidade}
            </div>
        </div>

        <div className="flex w-full justify-center items-center gap-3">
            <CalendarDays className="w-6 h-6 text-bah-purple"/>
            <div className="text-sm text-gray-600 dark:text-gray-300"> 
                {item.data}
            </div>
        </div>

        <div className="flex w-full justify-center items-center gap-3">
            <Clock9 className="w-6 h-6 text-bah-purple"/>
            <div className="text-sm text-gray-600 dark:text-gray-300"> 
                {item.horario}
            </div>
        </div>
      </div>
    </div>
  )
}

function IniciativaPage() {
  return (
    <>
      <Header />

      <section
        className="relative min-h-[280px] md:min-h-[360px] w-full bg-[url('../src/assets/background.png')] bg-cover bg-top md:bg-center bg-no-repeat md:bg-fixed flex items-end"
        aria-label="Hero da iniciativa"
      >
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/10 pointer-events-none" />

        <div className="w-full max-w-100vw mx-auto px-4 py-10 md:py-16">
          <div className="relative">
            <div className="absolute left-1/2 -translate-x-1/2 bottom-0 translate-y-4/3 md:translate-y-5/3 z-10">
              <button
                className="bg-purple-600 text-white px-6 md:px-10 py-2 md:py-3 rounded-xl text-sm md:text-base shadow-md hover:bg-purple-700 transition cursor-pointer"
                aria-label="Inscrever-se"
              >
                <span className="text-xl">Inscrever-se</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <main className="w-full max-w-6xl mx-auto px-4 py-10 md:py-16">
        <article className="prose prose-lg dark:prose-invert mx-auto text-center max-w-3xl">
          <h1 className="text-2xl md:text-4xl font-bold">Iniciativa X</h1>
          <p className="mt-2 text-base md:text-lg text-gray-700 dark:text-gray-300">
            Descrição do evento — aqui vai um parágrafo com informações principais. Pode conter até
            algumas linhas para explicar do que se trata a iniciativa, público alvo e outros detalhes
            relevantes.
          </p>
        </article>

        <section className="mt-10">
          <div className="flex justify-center items-center md:hidden">
            <Carousel className="w-full max-w-xs">
                <CarouselContent>
                    {horarios.map((h, index) => (
                        <CarouselItem key={index}>
                            <div className="p-1">
                                <HorarioCard item={h} />
                            </div>
                        </CarouselItem>
                    ))}
                </CarouselContent>
                <CarouselPrevious />
                <CarouselNext />
            </Carousel>
          </div>

          <div className="hidden md:grid md:grid-cols-3 md:gap-6">
            {horarios.map((h) => (
              <div key={h.id} className="px-2">
                <HorarioCard item={h} />
              </div>
            ))}
          </div>
        </section>
      </main>
    </>
  )
}

export default IniciativaPage