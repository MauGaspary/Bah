import * as React from 'react'

interface ValueCardProps {
  title: string
  desc: string
  Icon: React.ComponentType<React.SVGProps<SVGSVGElement>>
}

export function ValueCard({ title, desc, Icon }: ValueCardProps) {
  return (
    <div className="h-52 bg-bah-purple text-white rounded-xl p-4 md:p-6 flex flex-col gap-4 items-center justify-center shadow-lg">
      <div className="md:h-20 rounded-md text-bah-green flex flex-col items-center">
        <Icon className="w-6 h-6 md:w-14 md:h-14" />
        <h3 className="text-xl md:text-2xl font-bold">{title}</h3>
      </div>

      <p className="text-sm max-w-[230px] text-purple-100">{desc}</p>
    </div>
  )
}
