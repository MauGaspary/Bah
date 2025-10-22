import Header from '@/components/ui/Header/Header'
import SearchDropdown from '@/components/ui/Searchbar/SearchDropdown'

function HomePage() {
  const tags = [
    { name: 'Aceleração', value: 'aceleracao' },
    { name: 'Projetos', value: 'projetos' },
    { name: 'Investidores', value: 'investidores' },
    { name: 'Coworking', value: 'coworking' },
    { name: 'Mentorias', value: 'mentorias' },
  ]
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
        </section>
      </main>
    </>
  )
}

export default HomePage
