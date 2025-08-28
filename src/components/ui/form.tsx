import { AlertTriangle } from 'lucide-react'
import * as React from 'react'
import {
  FormProvider,
  useFormContext,
  Controller,
  type UseFormReturn,
  type FieldValues,
} from 'react-hook-form'

type FormProps<T extends FieldValues> = Omit<
  React.FormHTMLAttributes<HTMLFormElement>,
  'onSubmit'
> & {
  form: UseFormReturn<T>
  children: React.ReactNode
  onSubmit: (values: T) => void | Promise<void>
}

export function Form<T extends FieldValues>({
  form,
  children,
  onSubmit,
  ...props
}: FormProps<T>) {
  const handleInvalid = (errors: any) => {
    try {
      const first = Object.keys(errors || {})[0]
      if (first) {
        ;(form.setFocus as any)(first)
      }
    } catch (e) {}
  }

  return (
    <FormProvider {...form}>
      <form onSubmit={form.handleSubmit(onSubmit, handleInvalid)} {...props}>
        {children}
      </form>
    </FormProvider>
  )
}

export function FormField({
  name,
  children,
}: {
  name: string
  children: (opts: { field: any; fieldState: any }) => React.ReactNode
}) {
  const methods = useFormContext()

  return (
    <Controller
      name={name as any}
      control={methods.control}
      render={({ field, fieldState }) => <>{children({ field, fieldState })}</>}
    />
  )
}

export function FormItem({ className, ...props }: React.ComponentProps<'div'>) {
  return <div className={className} {...props} />
}

export function FormLabel({
  className,
  ...props
}: React.ComponentProps<'label'>) {
  return <label className={className} {...props} />
}

export function FormControl({
  children,
  ...props
}: React.ComponentProps<'div'>) {
  return <div {...props}>{children}</div>
}

export function FormMessage({ name }: { name: string }) {
  const { formState } = useFormContext()
  const error = (formState.errors as any)?.[name]

  if (!error) return null

  return (
    <div className="mt-2 flex items-start gap-2 bg-yellow-50 border border-yellow-200 text-yellow-900 rounded p-2 text-sm">
      <AlertTriangle className="w-4 h-4 text-yellow-700 mt-0.5 flex-shrink-0" />
      <div className="leading-tight">{String(error.message ?? error)}</div>
    </div>
  )
}

export type { UseFormReturn }
