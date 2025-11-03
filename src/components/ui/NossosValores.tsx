import { Lightbulb, Brush, Scale, Flame } from 'lucide-react'
import * as React from 'react'

import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from '@/components/ui/carousel'

const valores = [
  {
    title: "Inovação",
    desc: "Buscamos constantemente novas soluções",
    Icon: Lightbulb,
  },
  {
    title: "Criatividade",
    desc: "Estimulamos ideias originais",
    Icon: Brush,
  },
  {
    title: "Equilíbrio",
    desc: "Promovemos harmonia entre as atores",
    Icon: Scale,
  },
  {
    title: "Entusiasmo",
    desc: "Trabalhamos com paixão e energia",
    Icon: Flame,
  },
] 

function CarouselOrientation() {
  return (
    <Carousel
      opts={{
        align: "start",
      }}
      orientation="horizontal"
      className="w-full max-w-xs"
    >
      <CarouselContent className="-mt-1 flex items-center justify-start w-[300px] gap-4 ml-4">
        {valores.map((valor, index) => (
          <CarouselItem key={index} className="pt-1 !pl-0">
            <div className="p-0">
              <ValueCard
                key={index}
                title={valor.title}
                desc={valor.desc}
                Icon={valor.Icon}
              />
            </div>
          </CarouselItem>
        ))}
      </CarouselContent>
      <CarouselPrevious />
      <CarouselNext />
      
    </Carousel>
  )
}


function ValueCard({ title, desc, Icon }: { title: string; desc: string; Icon: React.ComponentType<React.SVGProps<SVGSVGElement>> }) {
  return (
    <div className="h-52 bg-bah-purple text-white rounded-xl p-4 md:p-6 flex flex-col gap-4 items-center justify-center shadow-lg">
      <div className=" md:h-20 rounded-md text-bah-green flex flex-col items-center">
        <Icon className="w-6 h-6 md:w-14 md:h-14" />
        <h3 className="text-xl md:text-2xl font-bold">{title}</h3>
      </div>

      <p className="text-sm max-w-[230px] text-purple-100">{desc}</p>
    </div>
  )
}

function NossosValores() {
    return (
      <>
        <div className="inline-block mb-5 md:mb-20">
            <h2 className="text-xl md:text-4xl font-semibold md:font-bold text-center">Nossos valores </h2>
            <div className='hidden md:block h-1 bg-bah-green w-[75%] mx-auto my-2' />
        </div>

        <section className="hidden md:block text-center min-h-screen">

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
            {valores.map((valor, index) => (
              <ValueCard
                key={index}
                title={valor.title}
                desc={valor.desc}
                Icon={valor.Icon}
              />
            ))}
          </div>
        </section>

        <section className="md:hidden text-center flex justify-center md:min-h-screen px-4 py-10">
          <CarouselOrientation />
        </section>
      </>
    )
}

export default NossosValores;