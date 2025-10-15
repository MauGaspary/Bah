import { useEffect, useMemo, useRef, useState } from 'react'
import type { CalendarEvent } from '../CalendarSection/CalendarSection'

export default function UpcomingCarousel({
  events,
  title = 'Próximos Eventos',
}: {
  events: CalendarEvent[]
  title?: string
}) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [activeIndex, setActiveIndex] = useState(0) // normalizado (0..events.length-1)
  const [activeVirtualIndex, setActiveVirtualIndex] = useState(0) // índice na lista virtual
  const virtualEvents = useMemo(() => (events.length ? [...events, ...events, ...events] : []), [events])
  const baseOffset = events.length // início do bloco central na lista virtual
  const scrollEndTimer = useRef<number | null>(null)
  const isProgrammatic = useRef(false)

  useEffect(() => {
    const el = containerRef.current
    if (!el || events.length === 0) return

    // Centraliza no bloco do meio ao iniciar
    const initVirtualIdx = baseOffset + 0
    centerToVirtualIndex(initVirtualIdx, false)
    setActiveVirtualIndex(initVirtualIdx)
    setActiveIndex(0)

    let ticking = false
    const onScroll = () => {
      if (ticking) return
      ticking = true
      requestAnimationFrame(() => {
        if (isProgrammatic.current) {
          ticking = false
          return
        }
        const cards = Array.from(
          el.querySelectorAll('article[data-virtual-index]')
        ) as HTMLElement[]
        if (cards.length === 0) {
          ticking = false
          return
        }
        const left = el.scrollLeft
        const center = left + el.clientWidth / 2
        let bestVirtualIdx = 0
        let bestDist = Infinity
        for (const card of cards) {
          const cardCenter = card.offsetLeft + card.clientWidth / 2
          const dist = Math.abs(cardCenter - center)
          if (dist < bestDist) {
            bestDist = dist
            bestVirtualIdx = Number(card.dataset.virtualIndex)
          }
        }

        setActiveVirtualIndex(bestVirtualIdx)
        const normalized = ((bestVirtualIdx % events.length) + events.length) % events.length
        setActiveIndex(normalized)

        // Debounce do recenter para suavizar (evita salto durante a rolagem)
        if (scrollEndTimer.current) {
          window.clearTimeout(scrollEndTimer.current)
        }
        scrollEndTimer.current = window.setTimeout(() => {
          if (bestVirtualIdx < baseOffset) {
            const newVIdx = bestVirtualIdx + events.length
            isProgrammatic.current = true
            centerToVirtualIndex(newVIdx, false)
            setActiveVirtualIndex(newVIdx)
            setActiveIndex(((newVIdx % events.length) + events.length) % events.length)
            // libera a flag no próximo frame
            requestAnimationFrame(() => {
              isProgrammatic.current = false
            })
          } else if (bestVirtualIdx >= baseOffset + events.length) {
            const newVIdx = bestVirtualIdx - events.length
            isProgrammatic.current = true
            centerToVirtualIndex(newVIdx, false)
            setActiveVirtualIndex(newVIdx)
            setActiveIndex(((newVIdx % events.length) + events.length) % events.length)
            requestAnimationFrame(() => {
              isProgrammatic.current = false
            })
          }
        }, 80)
        ticking = false
      })
    }
    el.addEventListener('scroll', onScroll, { passive: true } as any)
    // Trigger uma leitura inicial
    onScroll()
    return () => {
      el.removeEventListener('scroll', onScroll)
      if (scrollEndTimer.current) {
        window.clearTimeout(scrollEndTimer.current)
        scrollEndTimer.current = null
      }
    }
  }, [events])

  const centerToVirtualIndex = (vIdx: number, smooth: boolean) => {
    const el = containerRef.current
    if (!el) return
    const card = el.querySelector(
      `article[data-virtual-index="${vIdx}"]`
    ) as HTMLElement | null
    if (!card) return
    const targetLeft = card.offsetLeft - (el.clientWidth - card.clientWidth) / 2
    el.scrollTo({ left: targetLeft, behavior: smooth ? 'smooth' : 'auto' })
  }

  const scrollToIndex = (idx: number) => {
    if (events.length === 0) return
    const n = events.length
    // Escolhe o clone mais próximo do índice virtual atual para suavizar o scroll
    const c0 = baseOffset + idx - n
    const c1 = baseOffset + idx
    const c2 = baseOffset + idx + n
    const cur = activeVirtualIndex
    const candidates = [c0, c1, c2]
    let best = c1
    let bestDist = Math.abs(c1 - cur)
    for (const c of candidates) {
      const dist = Math.abs(c - cur)
      if (dist < bestDist) {
        best = c
        bestDist = dist
      }
    }
    centerToVirtualIndex(best, true)
  }

  return (
    <section className="md:hidden px-4 py-8">
      <h3 className="text-3xl md:text-4xl font-bold text-center font-mulish mb-3">
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

          {virtualEvents.map((ev, i) => (
            <article
              key={`${ev.id}-${i}`}
              data-virtual-index={i}
              className={`snap-center shrink-0 w-[88%] mx-auto transform transition-all duration-300 ${
                i === activeVirtualIndex
                  ? 'opacity-100 scale-100 z-10'
                  : 'opacity-70 scale-95 z-0 translate-y-1'
              }`}
            >
              <div
                className={`h-56 rounded-3xl overflow-hidden shadow-md transition-all duration-300 ${
                  i === activeVirtualIndex ? '' : 'blur-[2px]'
                }`}
              >
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
        {events.length > 0 && (
          <div className="mt-4 flex justify-center gap-2">
            {Array.from({ length: events.length }, (_, i) => i).map(i => {
              const key = events[i]?.id ?? i
              const activeDot = Math.min(activeIndex, events.length - 1)
              return (
                <span
                  key={key}
                  role="button"
                  aria-label={`Ir para card ${i + 1}`}
                  onClick={() => scrollToIndex(i)}
                  className={`h-2 w-2 rounded-full ${
                    i === activeDot ? 'bg-[#6B4BA9]' : 'bg-gray-300'
                  } cursor-pointer`}
                />
              )
            })}
          </div>
        )}
      </div>
    </section>
  )
}


