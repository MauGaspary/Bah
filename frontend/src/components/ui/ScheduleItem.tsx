import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import { CalendarIcon, Trash2Icon } from 'lucide-react'
import React from 'react'

import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import { Card, CardContent } from '@/components/ui/card'
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { HORARIO_TIPO_LABELS } from '@/enums/HorarioTipo'

type Option = { value: string; label: string }

const HOUR_OPTIONS: Option[] = [
  { value: '08:00', label: '08:00' },
  { value: '09:00', label: '09:00' },
  { value: '10:00', label: '10:00' },
  { value: '11:00', label: '11:00' },
  { value: '12:00', label: '12:00' },
  { value: '13:00', label: '13:00' },
  { value: '14:00', label: '14:00' },
  { value: '15:00', label: '15:00' },
  { value: '16:00', label: '16:00' },
  { value: '17:00', label: '17:00' },
]

interface ScheduleItemProps {
  index: number
  onRemove: (index: number) => void
}

const ScheduleItem: React.FC<ScheduleItemProps> = ({ index, onRemove }) => {
  return (
    <Card className="bg-gray-50 border-gray-100 mb-6">
      <CardContent className="p-4">
        <div className="flex justify-between items-start mb-3">
          <div className="text-callout-semibold font-sf-pro-text text-label-primary">
            Horário {index + 1}
          </div>

          <Button
            type="button"
            onClick={() => onRemove(index)}
            className="px-2 py-1 transition cursor-pointer flex items-center justify-center rounded-[8px] min-w-9 h-9"
            aria-label={`Remover horário ${index + 1}`}
            variant="ghost"
            size="sm"
            style={{ borderRadius: '10px' }}
          >
            <Trash2Icon className="w-4 h-4 text-red-500" />
          </Button>
        </div>

        {/* TimeSelect integrado */}
        <div className="flex flex-col space-y-4 lg:grid lg:grid-cols-3 lg:gap-4 lg:space-y-0 mb-4">
          {/* Data */}
          <div>
            <FormField name={`schedules.${index}.dia`}>
              {({ field }) => (
                <FormItem className="flex flex-col">
                  <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                    Data
                  </FormLabel>
                  <FormControl>
                    <Popover>
                      <PopoverTrigger asChild>
                        <Button
                          variant="ghost"
                          className={`min-w-1 w-full h-11 border px-4 border-gray-300 py-3 text-sm focus-visible:ring-2 focus-visible:ring-bah-purple focus-visible:border-transparent data-[state=open]:ring-2 data-[state=open]:ring-bah-purple data-[state=open]:border-transparent shadow-none justify-start text-left font-normal rounded-lg overflow-hidden ${field.value ? 'text-black' : 'text-gray-400'}`}
                        >
                          <CalendarIcon className="mr-2 h-4 w-4 flex-shrink-0" />
                          <span className="truncate">
                            {field.value
                              ? (() => {
                                  const raw = field.value as unknown
                                  const dateObj =
                                    typeof raw === 'string'
                                      ? new Date(raw + 'T00:00:00')
                                      : raw instanceof Date
                                        ? raw
                                        : undefined
                                  return dateObj && !isNaN(dateObj.getTime())
                                    ? format(dateObj, 'dd/MM/yyyy', {
                                        locale: ptBR,
                                      })
                                    : 'Selecione a data'
                                })()
                              : 'Selecione a data'}
                          </span>
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent
                        className="p-0 bg-white border-gray-200"
                        align="start"
                      >
                        <Calendar
                          mode="single"
                          selected={
                            field.value
                              ? typeof field.value === 'string'
                                ? new Date(field.value + 'T00:00:00')
                                : (field.value as Date)
                              : undefined
                          }
                          onSelect={date => {
                            if (date) {
                              const year = date.getFullYear()
                              const month = String(
                                date.getMonth() + 1
                              ).padStart(2, '0')
                              const day = String(date.getDate()).padStart(
                                2,
                                '0'
                              )
                              field.onChange(`${year}-${month}-${day}`)
                            } else {
                              field.onChange('')
                            }
                          }}
                          disabled={date => {
                            const today = new Date()
                            today.setHours(0, 0, 0, 0)
                            return date < today
                          }}
                          locale={ptBR}
                          className="bg-white w-full"
                        />
                      </PopoverContent>
                    </Popover>
                  </FormControl>
                  <FormMessage name={`schedules.${index}.dia`} />
                </FormItem>
              )}
            </FormField>
          </div>

          {/* Horário Início */}
          <div>
            <FormField name={`schedules.${index}.inicio`}>
              {({ field }) => (
                <FormItem className="flex flex-col">
                  <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                    Horário Início
                  </FormLabel>
                  <FormControl>
                    <Select value={field.value} onValueChange={field.onChange}>
                      <SelectTrigger
                        className={`w-full h-11 border px-4 border-gray-300 py-3 text-sm focus-visible:ring-2 focus-visible:ring-bah-purple focus-visible:border-transparent data-[state=open]:ring-2 data-[state=open]:ring-bah-purple data-[state=open]:border-transparent shadow-none rounded-lg ${field.value ? 'text-black' : 'text-gray-400'}`}
                      >
                        <SelectValue placeholder="Selecione o horário" />
                      </SelectTrigger>
                      <SelectContent className="border-bah-purple bg-white">
                        {HOUR_OPTIONS.map(opt => (
                          <SelectItem
                            key={opt.value}
                            value={opt.value}
                            className=" focus:bg-bah-purple focus:text-white"
                          >
                            {opt.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </FormControl>
                  <FormMessage name={`schedules.${index}.inicio`} />
                </FormItem>
              )}
            </FormField>
          </div>

          {/* Horário Fim */}
          <div>
            <FormField name={`schedules.${index}.fim`}>
              {({ field }) => (
                <FormItem className="flex flex-col">
                  <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                    Horário Fim
                  </FormLabel>
                  <FormControl>
                    <Select value={field.value} onValueChange={field.onChange}>
                      <SelectTrigger
                        className={`w-full h-11 border px-4 border-gray-300 py-3 text-sm focus-visible:ring-2 focus-visible:ring-bah-purple focus-visible:border-transparent data-[state=open]:ring-2 data-[state=open]:ring-bah-purple data-[state=open]:border-transparent shadow-none rounded-lg ${field.value ? 'text-black' : 'text-gray-400'}`}
                      >
                        <SelectValue placeholder="Selecione o horário" />
                      </SelectTrigger>
                      <SelectContent className="border-bah-purple bg-white">
                        {HOUR_OPTIONS.map(opt => (
                          <SelectItem
                            key={opt.value}
                            value={opt.value}
                            className=" focus:bg-bah-purple focus:text-white"
                          >
                            {opt.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </FormControl>
                  <FormMessage name={`schedules.${index}.fim`} />
                </FormItem>
              )}
            </FormField>
          </div>
        </div>

        {/* Tipo */}
        <div className="mt-2 w-full">
          <FormField name={`schedules.${index}.tipo`}>
            {({ field }) => (
              <FormItem className="flex flex-col w-full">
                <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                  Tipo
                </FormLabel>
                <FormControl>
                  <Select value={field.value} onValueChange={field.onChange}>
                    <SelectTrigger
                      className={`w-full h-11 border px-4 border-gray-300 py-3 text-sm focus-visible:ring-2 focus-visible:ring-bah-purple focus-visible:border-transparent data-[state=open]:ring-2 data-[state=open]:ring-bah-purple data-[state=open]:border-transparent shadow-none rounded-lg ${field.value ? 'text-black' : 'text-gray-400'}`}
                    >
                      <SelectValue placeholder="Selecione o tipo" />
                    </SelectTrigger>
                    <SelectContent className="border-bah-purple bg-white">
                      {Object.entries(HORARIO_TIPO_LABELS).map(
                        ([value, label]) => (
                          <SelectItem
                            key={value}
                            value={value}
                            className=" focus:bg-bah-purple focus:text-white"
                          >
                            {label}
                          </SelectItem>
                        )
                      )}
                    </SelectContent>
                  </Select>
                </FormControl>
                <FormMessage name={`schedules.${index}.tipo`} />
              </FormItem>
            )}
          </FormField>
        </div>
      </CardContent>
    </Card>
  )
}

export default ScheduleItem
