function SobreNos() {
  return (
    <div className="md:min-h-screen ">

      <main className="w-full max-w-6xl mx-auto px-4 md:py-20">
        <section className="text-center mb-5">
          <div className="display: inline-block">
            <h2 className="text-3xl md:text-4xl font-bold text-center">Sobre Nós</h2>
            <div className='h-1 bg-bah-green w-[75%] mx-auto my-2' />
          </div>
          <p className="mt-5 max-w-md mx-auto">
              Somos uma Plataforma de Inovação de Caxias do Sul que pensa de forma aberta, integrada e colaborativa.
            </p>
        

            <section className="mt-3 flex justify-center">
            <div className="w-full max-w-3xl">
                <div className="overflow-hidden rounded-md shadow-md">
                <img
                    src="/assets/sobre-nos.jpg"
                    alt="Equipe BAH"
                    className="w-full h-64 md:h-80 object-cover"
                />
                </div>
                <p className="text-center text-2xl md:text-xl text-bah-purple font-bold mt-3">"INTEGRAR PARA INOVAR"</p>
            </div>
            </section>

            <section className="mt-15 text-center">
            <h2 className="text-xl font-semibold">Nossa Missão</h2>
            <p className="mt-4 max-w-sm mx-auto">
                Fortalecer o empreendedorismo e disseminar a cultura de inovação para o desenvolvimento de Caxias do Sul,
                promovendo conexão, colaboração e desenvolvimento sustentável.
            </p>
            </section>
        </section>

        <div className='md:hidden h-0.5 bg-bah-purple w-full mx-auto' />
      </main>
    </div>
  )
}

export default SobreNos