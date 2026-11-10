import { Calendar1, MapPinned, CalendarDays, Clock9 } from "lucide-react"
import type { Iniciativa } from "@/interfaces/IIniciativas";

const formatTime = (timeString: string): string => {
  return timeString.slice(0, 5)
}

function HorarioCard({ item }: { item: Iniciativa['horarios'][number] }) {
    return (
      <div className="w-full max-w justify-center items-center md:max-w-sm mx-auto">
        <div className="h-full flex justify-center border border-purple-200 rounded-xl bg-white dark:bg-gray-800 py-3 flex-col items-start gap-5 shadow-sm">
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
                  {formatTime(item.hora_inicio)} -{' '}
                  {formatTime(item.hora_fim)}
              </div>
          </div>
        </div>
      </div>
    )
}

export default HorarioCard;