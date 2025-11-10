import Timeline from './Timeline'

function JourneySection() {
  return (
    <div>
      <div className="flex flex-col items-center gap-4">
        <h2 className="text-large-title md:text-4xl font-bold text-center">
          Jornada Empreendedora
        </h2>
        <hr className="w-72 md:w-80 border-0 bg-bah-green h-1 rounded-full "></hr>
        <p className="text-body-regular font-mulish text-label-primary text-center">
          Descubra em qual fase você está e encontre os recursos certos para
          avançar
        </p>
      </div>

      <div className="flex gap-6 md:gap-12 justify-center py-10 md:py-20 px-4">
        <Timeline />
      </div>
    </div>
  )
}

export default JourneySection
