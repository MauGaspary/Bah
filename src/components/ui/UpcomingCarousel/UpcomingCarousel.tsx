import { useEffect, useRef, useState } from 'react'
import type { CalendarEvent } from '../CalendarSection/CalendarSection'

export default function UpcomingCarousel({
  events,
  title = 'Próximos Eventos',
}: {
  events: CalendarEvent[]
  title?: string
}) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [activeIndex, setActiveIndex] = useState(0)

  useEffect(() => {
    const el = containerRef.current
    if (!el || events.length === 0) return
    const onScroll = () => {
      const cards = Array.from(
        el.querySelectorAll('article[data-index]')
      ) as HTMLElement[]
      if (cards.length === 0) return
      const left = el.scrollLeft
      let bestIdx = 0
      let bestDist = Infinity
      for (let i = 0; i < cards.length; i++) {
        const dist = Math.abs(cards[i].offsetLeft - left)
        if (dist < bestDist) {
          bestDist = dist
          bestIdx = i
        }
      }
      setActiveIndex(bestIdx)
    }
    el.addEventListener('scroll', onScroll, { passive: true } as any)
    onScroll()
    return () => {
      el.removeEventListener('scroll', onScroll)
    }
  }, [events])

  const scrollToIndex = (idx: number) => {
    const el = containerRef.current
    if (!el) return
    const card = el.querySelector(
      `article[data-index="${idx}"]`
    ) as HTMLElement | null
    if (card) {
      el.scrollTo({ left: card.offsetLeft, behavior: 'smooth' })
    }
  }

  return (
    <section className="md:hidden px-4 py-8">
      <h3 className="text-4xl font-bold text-center font-mulish mb-3">
        {title}
      </h3>
      <div className="h-1 w-40 bg-[#B9D77E] rounded-full mx-auto mb-6" />

      <div className="relative">
        <div
          ref={containerRef}
          className="flex gap-4 overflow-x-auto snap-x snap-mandatory pb-4 -mx-4 px-4"
          style={{ scrollbarWidth: 'none' }}
        >
          {events.length === 0 && (
            <div className="snap-center shrink-0 w-[88%] mx-auto">
              <div className="h-56 bg-gray-200 rounded-3xl" />
              <div className="mt-4 h-4 bg-gray-200 rounded w-2/3 mx-auto" />
              <div className="mt-2 h-4 bg-gray-100 rounded w-1/2 mx-auto" />
            </div>
          )}

          {events.map((ev, i) => (
            <article
              key={ev.id}
              data-index={i}
              className="snap-center shrink-0 w-[88%] mx-auto"
            >
              <div className="h-56 rounded-3xl overflow-hidden shadow-md">
                {ev.imageUrl ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={ev.imageUrl}
                    alt={ev.title}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <div className="h-full w-full bg-gradient-to-br from-[#7B60A7] to-[#B08ADF]" />
                )}
              </div>
              <h4 className="text-center mt-5 text-xl font-semibold">
                {ev.title}
              </h4>
              {ev.location && (
                <p className="text-center text-gray-600 text-sm">{ev.location}</p>
              )}
            </article>
          ))}
        </div>

        {/* Indicadores simples */}
        <div className="mt-4 flex justify-center gap-2">
          {(
            events.length === 0
              ? [0, 1, 2]
              : Array.from({ length: Math.min(events.length, 5) }, (_, i) => i)
          ).map((_, i) => {
            const key = events.length === 0 ? i : (events[i]?.id ?? i)
            const maxDots = Math.min(events.length || 3, 5)
            const activeDot = Math.min(activeIndex, maxDots - 1)
            return (
              <span
                key={key}
                role={events.length > 0 ? 'button' : undefined}
                aria-label={events.length > 0 ? `Ir para card ${i + 1}` : undefined}
                onClick={events.length > 0 ? () => scrollToIndex(i) : undefined}
                className={`h-2 w-2 rounded-full ${
                  i === activeDot ? 'bg-[#6B4BA9]' : 'bg-gray-300'
                } ${events.length > 0 ? 'cursor-pointer' : ''}`}
              />
            )
          })}
        </div>
      </div>
    </section>
  )
}


