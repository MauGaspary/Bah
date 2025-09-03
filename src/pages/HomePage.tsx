import { Search } from 'lucide-react'
import { useState } from 'react'

import Header from '@/components/ui/Header/Header'
import { Input } from '@/components/ui/Searchbar/Searchbar'

function HomePage() {
  const [searchQuery, setSearchQuery] = useState('')
  return (
    <>
      <Header variant="default" />
      <div
        className="min-h-screen h-full bg-[url('../src/assets/background.png')] bg-cover bg-top md:bg-center bg-no-repeat bg-fixed w-full flex items-center justify-center"
        id="home-section"
      >
        <div className="container mx-auto px-4 py-8 md:py-20">
          <img
            src="../src/assets/logo.png"
            alt="logo"
            className="w-32 md:w-40 h-24 md:h-30 mb-3 mx-auto hidden md:block"
          />
          <div className="flex items-center justify-center w-100 md:w-110 mx-auto ">
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
            <button className="bg-bah-purple/60 hover:bg-bah-purple/80 cursor-pointer text-white px-3 py-1.5 rounded-full text-sm font-medium border border-bah-purple/30 transition-all duration-200">
              Aceleração
            </button>
            <button className="bg-bah-purple/60 hover:bg-bah-purple/80 cursor-pointer text-white px-3 py-1.5 rounded-full text-sm font-medium border border-bah-purple/30 transition-all duration-200">
              Projetos
            </button>
            <button className="bg-bah-purple/60 hover:bg-bah-purple/80 cursor-pointer text-white px-3 py-1.5 rounded-full text-sm font-medium border border-bah-purple/30 transition-all duration-200">
              Investidores
            </button>
            <button className="bg-bah-purple/60 hover:bg-bah-purple/80 cursor-pointer text-white px-3 py-1.5 rounded-full text-sm font-medium border border-bah-purple/30 transition-all duration-200">
              Coworking
            </button>
            <button className="bg-bah-purple/60 hover:bg-bah-purple/80 cursor-pointer text-white px-3 py-1.5 rounded-full text-sm font-medium border border-bah-purple/30 transition-all duration-200">
              Mentorias
            </button>
          </div>
        </div>
      </div>
    </>
  )
}

export default HomePage
