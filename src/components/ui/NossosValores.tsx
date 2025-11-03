import { Lightbulb, Brush, Scale, Flame } from 'lucide-react'

function ValueCard({ title, desc, Icon }: { title: string; desc: string; Icon: any }) {
  return (
    <div className="bg-bah-purple text-white rounded-xl p-15 flex flex-col gap-4 items-center justify-center shadow-lg">
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
  <section className="text-center min-h-screen">
          <div className="display: inline-block mb-5 md:mb-20">
            <h2 className="text-xl md:text-4xl font-semibold md:font-bold text-center">Nossos valores </h2>
            <div className='hidden md:block h-1 bg-bah-green w-[75%] mx-auto my-2' />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
            <ValueCard
              title="Inovação"
              desc="Buscamos constantemente novas soluções"
              Icon={Lightbulb}
            />
            <ValueCard
              title="Criatividade"
              desc="Estimulamos ideias originais"
              Icon={Brush}
            />
            <ValueCard
              title="Equilíbrio"
              desc="Promovemos harmonia entre as atores"
              Icon={Scale}
            />
            <ValueCard
              title="Entusiasmo"
              desc="Trabalhamos com paixão e energia"
              Icon={Flame}
            />
          </div>
        </section>
    )
}

export default NossosValores;