import * as React from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'

import { cn } from '@/lib/utils'

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
  {
    variants: {
      variant: {
        primary:
        'bg-bah-blue hover:bg-bah-blue/90 text-white focus-visible:ring-bah-blue/50 rounded-button',
      success:
        'bg-bah-green hover:bg-bah-green/90 text-white focus-visible:ring-bah-green/50 rounded-button',
      error:
        'bg-error hover:bg-error/90 text-white focus-visible:ring-error/50 rounded-button',
      salmon:
        'bg-bah-red hover:bg-bah-red/90 text-white focus-visible:ring-bah-red/50 rounded-button',
      darkBlue:
        'bg-bah-dark-blue hover:bg-bah-dark-blue/90 text-white focus-visible:ring-bah-dark-blue/50 rounded-button',
      secondary:
        'bg-background-secondary hover:bg-gray3 text-label-primary border border-stroke-primary focus-visible:ring-gray/50 rounded-button',
      purple:
        'bg-bah-purple hover:bg-bah-purple/90 text-white focus-visible:ring-bah-purple/50 rounded-button',
      destructive:
        'bg-error hover:bg-error/90 text-white focus-visible:ring-error/50 rounded-button',
      outline:
        'border border-stroke-primary bg-background-primary hover:bg-background-secondary text-label-primary focus-visible:ring-gray/50 rounded-button',
      ghost:
        'hover:bg-bah-purple/30 text-label-primary focus-visible:ring-gray/50 rounded-lg',
      link: 'text-bah-blue underline-offset-4 hover:underline focus-visible:ring-bah-blue/50',
      list: 'border border-stroke-primary bg-background-primary hover:bg-background-secondary text-label-primary focus-visible:ring-gray/50 rounded-[5px]',
      },
      size: {
        default: 'h-9 px-4 py-2 has-[>svg]:px-3',
        sm: 'h-8 rounded-md gap-1.5 px-3 has-[>svg]:px-2.5',
        lg: 'h-10 rounded-md px-6 has-[>svg]:px-4',
        icon: 'size-9',
        'icon-sm': 'size-8',
        'icon-lg': 'size-10',
      },
    },
    defaultVariants: {
      variant: 'purple',
      size: 'default',
    },
  }
)

function Button({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: React.ComponentProps<'button'> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean
  }) {
  const Comp = asChild ? Slot : 'button'

  return (
    <Comp
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
