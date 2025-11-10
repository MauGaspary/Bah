import { useMemo, useState } from 'react'

type EventCategory =
  | 'networking'
  | 'feira'
  | 'meetup'
  | 'workshop'
  | 'hackathon'

export type CalendarEvent = {
  id: string
  title: string
  description?: string
  date: string // ISO date (yyyy-mm-dd)
  category: EventCategory
  location?: string
  imageUrl?: string
  featured?: boolean
}

const categoryName: Record<EventCategory, string> = {
  networking: 'Networking',
  feira: 'Feira',
  meetup: 'Meetup',
  workshop: 'Workshop',
  hackathon: 'Hackatons',
}

const categoryColor: Record<EventCategory, string> = {
  networking: 'bg-[#3BD1A2]',
  feira: 'bg-[#7382FF]',
  meetup: 'bg-[#FF7474]',
  workshop: 'bg-[#DDBCA8]',
  hackathon: 'bg-[#9AA8FF]',
}

function getMonthMatrix(viewDate: Date) {
  const firstDayOfMonth = new Date(viewDate.getFullYear(), viewDate.getMonth(), 1)
  const startDay = new Date(firstDayOfMonth)
  startDay.setDate(firstDayOfMonth.getDate() - ((firstDayOfMonth.getDay() + 6) % 7)) // start on Sunday

  const weeks: Date[][] = []
  for (let w = 0; w < 6; w++) {
    const week: Date[] = []
    for (let d = 0; d < 7; d++) {
      const cell = new Date(startDay)
      cell.setDate(startDay.getDate() + w * 7 + d)
      week.push(cell)
    }
    weeks.push(week)
  }
  return weeks
}

function formatMonthTitle(date: Date) {
  const formatter = new Intl.DateTimeFormat('pt-BR', { month: 'long' })
  const month = formatter.format(date)
  return month.charAt(0).toUpperCase() + month.slice(1)
}

function isSameDay(a: Date, b: Date) {
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  )
}

export function CalendarSection({
  events,
  today = new Date(),
}: {
  events: CalendarEvent[]
  today?: Date
}) {
  const [current, setCurrent] = useState<Date>(new Date(today))
  const [selected, setSelected] = useState<Date>(new Date(today))

  const monthWeeks = useMemo(() => getMonthMatrix(current), [current])
  const monthNumber = current.getMonth()

  const eventsByDay = useMemo(() => {
    const map = new Map<string, CalendarEvent[]>()
    for (const e of events) {
      map.set(e.date, [...(map.get(e.date) ?? []), e])
    }
    return map
  }, [events])

  const selectedEvents = useMemo(() => {
    const iso = selected.toISOString().slice(0, 10)
    return eventsByDay.get(iso) ?? []
  }, [eventsByDay, selected])

  const selectedTitle = useMemo(() => {
    if (isSameDay(selected, today)) return 'Eventos de Hoje'
    const fmt = new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: '2-digit' })
    return `Eventos de ${fmt.format(selected)}`
  }, [selected, today])

  const highlightEvents = useMemo(() => {
    const startIso = selected.toISOString().slice(0, 10)
    const end = new Date(selected)
    end.setDate(end.getDate() + 15)
    const endIso = end.toISOString().slice(0, 10)
    return events
      .filter(e => e.featured === true && e.date >= startIso && e.date <= endIso)
      .sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : 0))
      .slice(0, 3)
  }, [events, selected])

  return (
    <section className="container mx-auto px-4 md:px-6 py-6 md:py-10">
      {/* Legenda */}
      <div className="flex flex-wrap items-center gap-3 mb-4 md:mb-6">
        {Object.keys(categoryName).map(k => {
          const key = k as EventCategory
          return (
            <div key={key} className="flex items-center gap-2">
              <span className={`h-3 w-3 rounded-full ${categoryColor[key]}`} />
              <span className="text-sm text-gray-700">{categoryName[key]}</span>
            </div>
          )
        })}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-[1fr_360px] gap-6">
        {/* Calendário */}
        <div className="rounded-2xl overflow-hidden border border-gray-200 bg-white shadow-sm">
          <div className="bg-bah-purple text-white px-5 py-4 flex items-center justify-between">
            <button
              type="button"
              aria-label="Mês anterior"
              className="px-2 py-1 rounded hover:bg-white/10"
              onClick={() =>
                setCurrent(d => new Date(d.getFullYear(), d.getMonth() - 1, 1))
              }
            >
              ‹
            </button>
            <h3 className="text-lg font-semibold select-none">
              {formatMonthTitle(current)}
            </h3>
            <button
              type="button"
              aria-label="Próximo mês"
              className="px-2 py-1 rounded hover:bg-white/10"
              onClick={() =>
                setCurrent(d => new Date(d.getFullYear(), d.getMonth() + 1, 1))
              }
            >
              ›
            </button>
          </div>

          <div className="grid grid-cols-7 text-center text-gray-500 text-xs md:text-sm py-3">
            {['DOM', 'SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB'].map(w => (
              <div key={w} className="uppercase tracking-wide">
                {w}
              </div>
            ))}
          </div>

          <div className="grid grid-cols-7">
            {monthWeeks.map((week, i) => (
              <div key={i} className="contents">
                {week.map(day => {
                  const inMonth = day.getMonth() === monthNumber
                  const iso = day.toISOString().slice(0, 10)
                  const dayEvents = eventsByDay.get(iso) ?? []
                  const isToday = isSameDay(day, today)
                  const isSelected = isSameDay(day, selected)
                  return (
                    <div
                      key={iso}
                      className={`h-20 md:h-28 relative border-t border-gray-100 pt-2 text-sm cursor-pointer ${
                        inMonth ? 'text-gray-900' : 'text-gray-400'
                      } ${isSelected ? 'bg-bah-purple/20 rounded-2xl' : ''}`}
                      onClick={() => {
                        setSelected(new Date(day))
                        if (day.getMonth() !== monthNumber) {
                          setCurrent(new Date(day.getFullYear(), day.getMonth(), 1))
                        }
                      }}
                    >
                      <div
                        className={`w-8 h-8 flex items-center justify-center rounded-full ml-2 ${
                          isSelected
                            ? 'bg-bah-purple text-white'
                            : isToday
                            ? 'bg-[#E8F3C7] text-black'
                            : ''
                        }`}
                      >
                        {day.getDate()}
                      </div>

                      {/* marcadores de eventos (até 3 bolinhas) */}
                      <div className="absolute left-2 bottom-2 flex gap-1">
                        {dayEvents.slice(0, 3).map(e => (
                          <span
                            key={e.id}
                            className={`h-2.5 w-2.5 rounded-full ${categoryColor[e.category]}`}
                            title={e.title}
                          />
                        ))}
                      </div>
                    </div>
                  )
                })}
              </div>
            ))}
          </div>
        </div>

        {/* Lateral: Destaques + Hoje */}
        <aside className="space-y-6">
          <div className="rounded-2xl overflow-hidden border border-gray-200 bg-white shadow-sm">
            <div className="bg-bah-purple text-white px-5 py-3 font-semibold">
              Eventos Destaque
            </div>
            <div className="p-4 space-y-4">
              {highlightEvents.length === 0 && (
                <p className="text-sm text-gray-500">Nenhum destaque disponível.</p>
              )}
              {highlightEvents.map(e => (
                <div
                  key={e.id}
                  className="flex gap-3 rounded-xl border border-gray-200 p-3"
                >
                  <div
                    className={`w-1 rounded-lg ${categoryColor[e.category]}`}
                  />
                  <div className="flex-1">
                    <p className="text-xs text-gray-500">
                      {categoryName[e.category]}
                    </p>
                    <h4 className="text-sm font-semibold text-gray-900">
                      {e.title}
                    </h4>
                    {e.description && (
                      <p className="text-xs text-gray-600 line-clamp-2">
                        {e.description}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl overflow-hidden border border-gray-200 bg-white shadow-sm">
            <div className="bg-bah-purple text-white px-5 py-3 font-semibold">
              {selectedTitle}
            </div>
            <div className="p-4 space-y-4">
              {selectedEvents.length === 0 && (
                <p className="text-sm text-gray-500">Nenhum evento neste dia.</p>
              )}
              {selectedEvents.map(e => (
                <div
                  key={e.id}
                  className="flex gap-3 rounded-xl border border-gray-200 p-3"
                >
                  <div
                    className={`w-1 rounded-lg ${categoryColor[e.category]}`}
                  />
                  <div className="flex-1">
                    <p className="text-xs text-gray-500">
                      {categoryName[e.category]}
                    </p>
                    <h4 className="text-sm font-semibold text-gray-900">
                      {e.title}
                    </h4>
                    {e.description && (
                      <p className="text-xs text-gray-600 line-clamp-2">
                        {e.description}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </aside>
      </div>
    </section>
  )
}

export default CalendarSection


