import * as React from 'react'

import { cn } from '@/lib/utils'

type InputProps = React.ComponentProps<'input'> & {
  className?: string
  trailing?: React.ReactNode
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, trailing, ...props }, ref) => {
    return (
      <div className={cn('relative w-full', className)}>
        <input
          ref={ref}
          className={cn(
            'w-full px-4 py-3 border border-gray-300 rounded-lg outline-none focus:outline-none focus-visible:ring-2 focus-visible:ring-bah-purple focus-visible:border-transparent ring-offset-0',
            trailing ? 'pr-10' : ''
          )}
          {...props}
        />
        {trailing && (
          <div className="absolute right-3 inset-y-0 flex items-center">
            {trailing}
          </div>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'

export { Input }
