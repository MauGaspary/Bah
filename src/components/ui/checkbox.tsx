import * as React from 'react'

import { cn } from '@/lib/utils'

type CheckboxProps = React.ComponentProps<'input'> & { label?: string }

function Checkbox({ className, label, ...props }: CheckboxProps) {
  return (
    <label className="inline-flex items-center cursor-pointer">
      <input
        type="checkbox"
        className={cn(
          'w-4 h-4 text-bah-purple border-gray-300 rounded cursor-pointer focus:ring-bah-purple accent-bah-purple',
          className
        )}
        {...props}
      />
      {label && <span className="ml-2 text-sm text-gray-700">{label}</span>}
    </label>
  )
}

export { Checkbox }
