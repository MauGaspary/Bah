import { Lightbulb, Brush, Scale, Flame } from 'lucide-react'
import { ValueCard } from '@/components/ui/ValueCard'
import { ValoresCarousel } from '@/components/ui/ValoresCarousel'

const valores = [
  {
    title: 'Inovação',
    desc: 'Buscamos constantemente novas soluções',
    Icon: Lightbulb,
  },
  {
    title: 'Criatividade',
    desc: 'Estimulamos ideias originais',
    Icon: Brush,
  },
  {
    title: 'Equilíbrio',
    desc: 'Promovemos harmonia entre as atores',
    Icon: Scale,
  },
  {
    title: 'Entusiasmo',
    desc: 'Trabalhamos com paixão e energia',
    Icon: Flame,
  },
]

function NossosValoresPage() {
  return (
    <>
      <div className="inline-block mb-5 md:mb-10">
        <h2 className="text-xl md:text-4xl font-semibold md:font-bold text-center">
          Nossos valores
        </h2>
        <div className="hidden md:block h-1 bg-bah-green w-[75%] mx-auto my-2" />
      </div>

      <section className="hidden md:block text-center">
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

      <section className="md:hidden text-center flex justify-center px-4 py-10">
        <ValoresCarousel valores={valores} />
      </section>
    </>
  )
}

export default NossosValoresPage
