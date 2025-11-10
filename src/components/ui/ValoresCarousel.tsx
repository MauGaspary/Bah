import {
  Carousel,
  CarouselContent,
  CarouselItem,
} from '@/components/ui/carousel'
import { ValueCard } from '@/components/ui/ValueCard'
import * as React from 'react'

interface Valor {
  title: string
  desc: string
  Icon: React.ComponentType<React.SVGProps<SVGSVGElement>>
}

interface ValoresCarouselProps {
  valores: Valor[]
}

export function ValoresCarousel({ valores }: ValoresCarouselProps) {
  return (
    <div className="w-full overflow-hidden -mx-4">
      <Carousel
        opts={{
          align: 'start',
          loop: true,
        }}
        orientation="horizontal"
        className="w-full"
      >
        <CarouselContent className="-ml-2">
          {valores.map((valor, index) => (
            <CarouselItem key={index} className="pl-2 basis-[90%]">
              <ValueCard
                title={valor.title}
                desc={valor.desc}
                Icon={valor.Icon}
              />
            </CarouselItem>
          ))}
        </CarouselContent>
      </Carousel>
    </div>
  )
}
