import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'
import * as React from 'react'

import { cn } from '@/lib/utils'

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-3 whitespace-nowrap text-callout-semibold font-sf-pro transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-5 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
  {
    variants: {
      variant: {
        primary:
          'bg-bah-blue hover:bg-bah-blue/90 text-white focus-visible:ring-bah-blue/50 rounded-button',
        success:
          'bg-bah-green hover:bg-bah-green/90 text-white focus-visible:ring-bah-green/50 rounded-button',
        secondary:
          'bg-background-secondary hover:bg-gray3 text-label-primary border border-stroke-primary focus-visible:ring-gray/50 rounded-button',
        purple:
          'bg-bah-purple hover:bg-bah-purple/90 text-white focus-visible:ring-bah-purple/50 rounded-button',
        destructive:
          'bg-error hover:bg-error/90 text-white focus-visible:ring-error/50 rounded-button',
        outline:
          'border border-stroke-primary bg-background-primary hover:bg-background-secondary text-label-primary focus-visible:ring-gray/50 rounded-button',
        ghost:
          'hover:bg-background-secondary text-label-primary focus-visible:ring-gray/50 rounded-button',
        link: 'text-bah-blue underline-offset-4 hover:underline focus-visible:ring-bah-blue/50',
      },
      size: {
        sm: 'h-8 px-3 py-1.5 text-footnote min-w-[120px] has-[>svg]:px-2.5',
        default: 'h-[52px] px-4 py-2 min-w-[197px] has-[>svg]:px-3',
        lg: 'h-12 px-6 py-3 text-body-semibold min-w-[220px] has-[>svg]:px-4',
      },
    },
    defaultVariants: {
      variant: 'primary',
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
