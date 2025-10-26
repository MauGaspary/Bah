import React, { useEffect, useRef, useState, type KeyboardEvent } from 'react'
import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import toast, { Toaster } from 'react-hot-toast'
import { Camera, Star, Trash2Icon } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form'
import SidebarAdm from '@/components/ui/sidebar'
import * as iniciativasService from '@/service/iniciativas'

type Option = { value: string; label: string }

const HOUR_OPTIONS: Option[] = [
  { value: '', label: 'Selecione o horário' },
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

const DAY_OPTIONS: Option[] = [
  { value: '', label: 'Selecione o dia' },
  { value: 'segunda', label: 'Segunda-feira' },
  { value: 'terca', label: 'Terça-feira' },
  { value: 'quarta', label: 'Quarta-feira' },
  { value: 'quinta', label: 'Quinta-feira' },
  { value: 'sexta', label: 'Sexta-feira' },
  { value: 'sabado', label: 'Sábado' },
  { value: 'domingo', label: 'Domingo' },
]

interface TimeSelectProps {
  dayValue: string
  startValue: string
  endValue: string
  onDayChange: (v: string) => void
  onStartChange: (v: string) => void
  onEndChange: (v: string) => void
}

const TimeSelect: React.FC<TimeSelectProps> = ({
  dayValue,
  startValue,
  endValue,
  onDayChange,
  onStartChange,
  onEndChange,
}) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <div>
        <Label className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
          Dia
        </Label>
        <select
          value={dayValue ?? ''}
          onChange={e => onDayChange(e.target.value)}
          className="w-full py-3 border-2 border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-2 focus:ring-bah-purple focus:border-transparent cursor-pointer"
        >
          {DAY_OPTIONS.map(opt => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <Label className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
          Horário Início
        </Label>
        <select
          value={startValue ?? ''}
          onChange={e => onStartChange(e.target.value)}
          className="w-full py-3 border-2 border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-2 focus:ring-bah-purple focus:border-transparent cursor-pointer"
        >
          {HOUR_OPTIONS.map(opt => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <Label className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
          Horário Fim
        </Label>
        <select
          value={endValue ?? ''}
          onChange={e => onEndChange(e.target.value)}
          className="w-full py-3 border-2 border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-2 focus:ring-bah-purple focus:border-transparent cursor-pointer"
        >
          {HOUR_OPTIONS.map(opt => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}

const scheduleSchema = z.object({
  id: z.string().optional(),
  dia: z.string().min(1, 'O dia é obrigatório.'),
  inicio: z.string().min(1, 'O horário de início é obrigatório.'),
  fim: z.string().min(1, 'O horário de fim é obrigatório.'),
  tipo: z.string().min(1, 'O tipo de horário é obrigatório.'),
})

const initiativeSchema = z.object({
  titulo: z.string().min(3, 'O título deve ter pelo menos 3 caracteres.'),
  local: z.string().min(3, 'O local deve ter pelo menos 3 caracteres.'),
  link1: z
    .string()
    .url('O link 1 deve ser uma URL válida.')
    .optional()
    .or(z.literal('')),
  link2: z
    .string()
    .url('O link 2 deve ser uma URL válida.')
    .optional()
    .or(z.literal('')),
  organizador: z.string().min(1, 'O organizador é obrigatório.'),
  descricao: z
    .string()
    .min(10, 'A descrição deve ter pelo menos 10 caracteres.'),
  descricoes_extras: z
    .array(z.string().min(10, 'A descrição deve ter pelo menos 10 caracteres.'))
    .optional(),
  isAtivo: z.boolean(),
  tags: z.array(z.string()).min(1, 'Adicione pelo menos uma tag.'),
  schedules: z.array(scheduleSchema),
  newTag: z.string().optional(),
  foto: z.any().optional(),
})

type InitiativeFormData = z.infer<typeof initiativeSchema>

const ScheduleItem: React.FC<{
  index: number
  onRemove: (index: number) => void
  errors?: any
}> = ({ index, onRemove, errors }) => {
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
            className="px-2 py-1 transition cursor-pointer flex items-center justify-center"
            aria-label={`Remover horário ${index + 1}`}
            variant="ghost"
            size="sm"
            style={{ borderRadius: '8px', minWidth: '36px', height: '36px' }}
          >
            <Trash2Icon className="w-4 h-4 text-red-500" />
          </Button>
        </div>

        <FormField name={`schedules.${index}.dia`}>
          {({ field: dayField }) => (
            <FormField name={`schedules.${index}.inicio`}>
              {({ field: inicioField }) => (
                <FormField name={`schedules.${index}.fim`}>
                  {({ field: fimField }) => (
                    <>
                      <TimeSelect
                        dayValue={dayField.value}
                        startValue={inicioField.value}
                        endValue={fimField.value}
                        onDayChange={dayField.onChange}
                        onStartChange={inicioField.onChange}
                        onEndChange={fimField.onChange}
                      />

                      <div className="mt-2 grid grid-cols-1 sm:grid-cols-3 gap-3">
                        {errors?.[index]?.dia && (
                          <p className="text-red-500 text-xs">
                            {errors[index].dia.message}
                          </p>
                        )}
                        {errors?.[index]?.inicio && (
                          <p className="text-red-500 text-xs">
                            {errors[index].inicio.message}
                          </p>
                        )}
                        {errors?.[index]?.fim && (
                          <p className="text-red-500 text-xs">
                            {errors[index].fim.message}
                          </p>
                        )}
                      </div>
                    </>
                  )}
                </FormField>
              )}
            </FormField>
          )}
        </FormField>

        <div className="mt-2">
          <FormField name={`schedules.${index}.tipo`}>
            {({ field }) => (
              <FormItem className="flex flex-col">
                <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                  Tipo
                </FormLabel>
                <FormControl>
                  <select
                    value={field.value ?? ''}
                    onChange={field.onChange}
                    className="w-full py-3 border-2 border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-2 focus:ring-bah-purple focus:border-transparent cursor-pointer"
                  >
                    <option value="">Selecione o tipo</option>
                    <option value="presencial">Presencial</option>
                    <option value="online">Online</option>
                    <option value="hibrido">Híbrido</option>
                  </select>
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

export default function FormIniciativa() {
  const [isEditing, setIsEditing] = useState(false)
  const MAX_DESCRICOES = 5

  const form = useForm<InitiativeFormData>({
    resolver: zodResolver(initiativeSchema),
    defaultValues: {
      titulo: '',
      local: '',
      link1: '',
      link2: '',
      organizador: '',
      descricao: '',
      descricoes_extras: [],
      isAtivo: false,
      tags: [],
      schedules: [],
      newTag: '',
      foto: undefined,
    },
  })

  const {
    register,
    control,
    reset,
    getValues,
    setValue,
    watch,
    formState: { errors, isSubmitting },
  } = form

  const organizadorValue = watch('organizador')
  const {
    fields: tagFields,
    append: appendTag,
    remove: removeTag,
  } = useFieldArray({ control, name: 'tags' })
  const {
    fields: scheduleFields,
    append: appendSchedule,
    remove: removeSchedule,
  } = useFieldArray({ control, name: 'schedules' })

  const {
    fields: descricaoFields,
    append: appendDescricao,
    remove: removeDescricao,
  } = useFieldArray({ control, name: 'descricoes_extras' })

  const descricoesListRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const el = descricoesListRef.current
    if (!el) return
    const maxScrollTop = Math.max(0, el.scrollHeight - el.clientHeight)
    if (el.scrollTop > maxScrollTop) {
      el.scrollTop = maxScrollTop
    }
  }, [descricaoFields.length])

  const handleNewTagKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      const newTagValue = getValues('newTag')?.trim()
      if (newTagValue && !getValues('tags').includes(newTagValue)) {
        appendTag(newTagValue)
        setValue('newTag', '')
      }
    }
  }

  const onSubmit = async (data: InitiativeFormData) => {
    const payload = {
      titulo: data.titulo,
      descricao: data.descricao,
      organizador_id: data.organizador || '',
      link: data.link1 || data.link2 || '',
      local: data.local,
      imagem_url: '',
      destaque: data.isAtivo,
      horarios: [],
      tag_ids: [],
      descricoes_extras: data.descricoes_extras ?? [],
    }
    try {
      await iniciativasService.createIniciativa(payload)
      toast.success(
        isEditing
          ? 'Iniciativa atualizada com sucesso!'
          : 'Iniciativa criada com sucesso!'
      )
    } catch (e) {
      toast.error('Falha ao salvar a iniciativa')
    }
  }

  useEffect(() => {
    if (isEditing) {
      const dadosDoBackend: InitiativeFormData = {
        titulo: 'Iniciativa de Exemplo',
        local: 'Online',
        link1: 'https://site.com',
        link2: '',
        organizador: 'Equipe BAH',
        descricao: 'Descrição de exemplo para o modo de edição.',
        descricoes_extras: ['Descrição extra 1'],
        isAtivo: false,
        tags: ['React', 'TypeScript'],
        schedules: [
          {
            id: '1',
            dia: 'segunda',
            inicio: '09:00',
            fim: '11:00',
            tipo: 'online',
          },
        ],
        newTag: '',
        foto: undefined,
      }
      reset(dadosDoBackend)
    } else {
      reset({
        titulo: '',
        local: '',
        link1: '',
        link2: '',
        organizador: '',
        descricao: '',
        descricoes_extras: [],
        isAtivo: false,
        tags: [],
        schedules: [],
        newTag: '',
        foto: undefined,
      })
    }
  }, [isEditing, reset])

  return (
    <div className="flex h-screen w-full">
      <SidebarAdm />
      <main className="flex-1 p-6 bg-gray-50 overflow-y-auto w-full">
        <Toaster position="top-right" reverseOrder={false} />

        <header className="mb-6 flex justify-between items-center">
          <div className="text-left">
            <h1 className="text-large-title font-mulish text-[#5a2d86]">
              {isEditing ? 'Editar Iniciativa' : 'Criar Iniciativa'}
            </h1>
            <p className="text-body-regular font-sf-pro text-label-secondary">
              {isEditing ? 'Edite sua iniciativa' : 'Crie aqui sua nova iniciativa'}
            </p>
          </div>
          <Button
            type="button"
            onClick={() => setIsEditing(!isEditing)}
            variant="secondary"
            size="sm"
            className="min-w-fit cursor-pointer"
          >
            {isEditing ? 'Cancelar Edição' : 'Editar'}
          </Button>
        </header>

        <Form<InitiativeFormData> form={form} onSubmit={onSubmit} className="w-full">
          <section className="w-full max-w-none">
            <Card className="bg-white border-gray-100 shadow-sm w-full">
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle className="text-title3-semibold font-sf-pro-text text-label-primary">
                    Detalhes da Iniciativa
                  </CardTitle>
                  <div className="flex items-center gap-2">
                    <Star
                      className={`w-5 h-5 ${watch('isAtivo') ? 'text-black fill-black' : 'text-gray-400 fill-gray-400'}`}
                    />
                    <FormField name="isAtivo">
                      {({ field }) => (
                        <Switch
                          checked={field.value}
                          onCheckedChange={field.onChange}
                          className="data-[state=checked]:bg-green-500 data-[state=unchecked]:bg-gray-300 [&>span]:bg-white [&>span]:shadow-lg cursor-pointer"
                        />
                      )}
                    </FormField>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 gap-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <FormField name="titulo">
                      {({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                            Título
                          </FormLabel>
                          <FormControl>
                            <Input
                              {...field}
                              placeholder="Digite o título"
                              className="py-3 rounded-[0.8rem] text-sm placeholder:text-gray-400"
                            />
                          </FormControl>
                          <FormMessage name="titulo" />
                        </FormItem>
                      )}
                    </FormField>

                    <FormField name="local">
                      {({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                            Local
                          </FormLabel>
                          <FormControl>
                            <Input
                              {...field}
                              placeholder="Digite o local"
                              className="py-3 rounded-[0.8rem] text-sm placeholder:text-gray-400"
                            />
                          </FormControl>
                          <FormMessage name="local" />
                        </FormItem>
                      )}
                    </FormField>

                    <FormField name="link1">
                      {({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                            Link 1
                          </FormLabel>
                          <FormControl>
                            <Input
                              {...field}
                              placeholder="https://exemplo.com"
                              className="py-3 rounded-[0.8rem] text-sm placeholder:text-gray-400"
                            />
                          </FormControl>
                          <FormMessage name="link1" />
                        </FormItem>
                      )}
                    </FormField>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <FormField name="link2">
                      {({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                            Link 2
                          </FormLabel>
                          <FormControl>
                            <Input
                              {...field}
                              placeholder="https://linkedin.com/exemplo"
                              className="py-3 rounded-[0.8rem] text-sm placeholder:text-gray-400"
                            />
                          </FormControl>
                          <FormMessage name="link2" />
                        </FormItem>
                      )}
                    </FormField>
                    <FormField name="organizador">
                      {({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-5">
                            Organizador
                          </FormLabel>
                          <FormControl>
                            <div className="relative">
                              <select
                                {...field}
                                className={`w-full py-3 pl-3 pr-10 border-2 border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-2 focus:ring-bah-purple focus:border-transparent cursor-pointer appearance-none ${!organizadorValue ? 'text-gray-400' : 'text-black'}`}
                              >
                                <option value="" disabled>
                                  Selecione
                                </option>
                                <option value="Equipe BAH">Equipe BAH</option>
                              </select>
                              <div className="absolute inset-y-0 right-3 flex items-center pointer-events-none">
                                <svg
                                  className="w-4 h-4 text-gray-400"
                                  fill="none"
                                  stroke="currentColor"
                                  viewBox="0 0 24 24"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M19 9l-7 7-7-7"
                                  />
                                </svg>
                              </div>
                            </div>
                          </FormControl>
                          <FormMessage name="organizador" />
                        </FormItem>
                      )}
                    </FormField>
                  </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <FormField name="descricao">
                      {({ field }) => (
                        <FormItem className="md:col-span-2 flex flex-col">
                          <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                            Descrição
                          </FormLabel>
                          <FormControl>
                            <Textarea
                              {...field}
                              placeholder="Digite a descrição"
                              className="py-3 px-3 rounded-[0.8rem] text-sm h-40 resize-y placeholder:text-gray-400 border-2 border-gray-200 focus:outline-none focus:ring-0 focus:border-bah-purple focus-visible:ring-0 focus-visible:ring-offset-0"
                            />
                          </FormControl>
                          <FormMessage name="descricao" />
                        </FormItem>
                      )}
                    </FormField>

                    <FormField name="tags">
                      {() => (
                        <FormItem className="md:col-span-1 flex flex-col">
                          <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                            Tags
                          </FormLabel>
                          <FormControl>
                            <div className="w-full border-2 border-gray-200 rounded-[1rem] h-[10rem] p-3 flex flex-col">
                              <div className="flex-1 overflow-y-auto pr-1 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent">
                                <div className="flex flex-wrap gap-2">
                                  {tagFields.map((field, index) => (
                                    <span
                                      key={field.id}
                                      className="inline-flex items-center gap-1 bg-lime-200 text-lime-800 text-sm font-medium pl-3 pr-1 py-1 rounded-full"
                                    >
                                      {getValues(`tags.${index}`)}
                                      <Button
                                        type="button"
                                        onClick={() => removeTag(index)}
                                        className="text-lime-400 hover:text-lime-600 hover:ring-0 focus:ring-0 focus:outline-none w-5 h-5 p-0 min-w-5 flex items-center justify-center cursor-pointer"
                                        aria-label={`Remover tag ${getValues(`tags.${index}`)}`}
                                        variant="ghost"
                                        size="sm"
                                      >
                                        ✕
                                      </Button>
                                    </span>
                                  ))}
                                </div>
                              </div>
                              <Input
                                {...register('newTag')}
                                onKeyDown={handleNewTagKeyDown}
                                placeholder="Adicionar tag..."
                                className="w-full pt-2 border-t border-gray-200 text-sm focus:outline-none bg-transparent placeholder:text-gray-400 flex-shrink-0"
                              />
                            </div>
                          </FormControl>
                          <FormMessage name="tags" />
                        </FormItem>
                      )}
                    </FormField>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>

          <section className="w-full max-w-none mt-8">
            <Card className="bg-white border-gray-100 shadow-sm w-full">
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle className="text-title3-semibold font-sf-pro-text text-label-primary">
                    Descrições extras
                  </CardTitle>
                  <div className="flex flex-col items-center">
                    <p className="text-footnote font-sf-pro text-label-primary mb-1">
                      Clique para adicionar
                    </p>
                    <Button
                      type="button"
                      onClick={() =>
                        descricaoFields.length < MAX_DESCRICOES && appendDescricao('')
                      }
                      disabled={descricaoFields.length >= MAX_DESCRICOES}
                      className="bg-[#f2f2f7] text-[#85858b] hover:bg-gray-300 flex items-center justify-center cursor-pointer"
                      style={{
                        minWidth: '130px',
                        height: '30px',
                        borderRadius: '10px',
                        padding: 0,
                      }}
                      aria-label="Adicionar descrição extra"
                    >
                      +
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div ref={descricoesListRef} className="grid grid-cols-1 md:grid-cols-2 gap-6 max-h-[520px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-gray-300">
                  {descricaoFields.length === 0 && (
                    <div className="col-span-full text-callout-regular font-sf-pro text-label-secondary">
                      Nenhuma descrição extra adicionada — clique em + para adicionar.
                    </div>
                  )}

                  {descricaoFields.map((field, index) => (
                    <Card key={field.id} className="bg-gray-50 border-gray-100">
                      <CardContent className="p-4">
                        <div className="flex justify-between items-start mb-3">
                          <div className="text-callout-semibold font-sf-pro-text text-label-primary">
                            Descrição extra {index + 1}
                          </div>
                          <Button
                            type="button"
                            onClick={() => removeDescricao(index)}
                            className="text-white px-3 py-1 transition cursor-pointer"
                            aria-label={`Remover descrição extra ${index + 1}`}
                            variant="destructive"
                            size="sm"
                            style={{ borderRadius: '10px' }}
                          >
                            Remover
                          </Button>
                        </div>

                        <FormField name={`descricoes_extras.${index}`}>
                          {({ field }) => (
                            <FormItem className="flex flex-col">
                              <FormControl>
                                <Textarea
                                  {...field}
                                  placeholder="Digite a descrição"
                                  className="py-3 px-3 rounded-[0.8rem] text-sm h-40 resize-y placeholder:text-gray-400 border-2 border-gray-200 focus:outline-none focus:ring-0 focus:border-bah-purple focus-visible:ring-0 focus-visible:ring-offset-0"
                                />
                              </FormControl>
                              <FormMessage name={`descricoes_extras.${index}`} />
                            </FormItem>
                          )}
                        </FormField>
                      </CardContent>
                    </Card>
                  ))}
                </div>
                {descricaoFields.length >= MAX_DESCRICOES && (
                  <p className="text-xs text-label-secondary mt-3">
                    Limite de {MAX_DESCRICOES} descrições atingido.
                  </p>
                )}
              </CardContent>
            </Card>
          </section>

          <section className="w-full max-w-none mt-8">
            <Card className="bg-white border-gray-100 shadow-sm w-full">
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle className="text-title3-semibold font-sf-pro-text text-label-primary">
                    Horários
                  </CardTitle>

                  <div className="flex flex-col items-center">
                    <p className="text-footnote font-sf-pro text-label-primary mb-1">
                      Clique para adicionar
                    </p>
                    <Button
                      type="button"
                      onClick={() =>
                        appendSchedule({
                          dia: '',
                          inicio: '',
                          fim: '',
                          tipo: '',
                        })
                      }
                      className="bg-[#f2f2f7] text-[#85858b] hover:bg-gray-300 flex items-center justify-center cursor-pointer"
                      style={{
                        minWidth: '130px',
                        height: '30px',
                        borderRadius: '10px',
                        padding: 0,
                      }}
                      aria-label="Adicionar horário"
                    >
                      +
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-h-[520px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-gray-300">
                  {scheduleFields.length === 0 && (
                    <div className="col-span-full text-callout-regular font-sf-pro text-label-secondary">
                      Nenhum horário adicionado — clique em + para adicionar.
                    </div>
                  )}

                  {scheduleFields.map((field, index) => (
                    <ScheduleItem
                      key={field.id}
                      index={index}
                      onRemove={removeSchedule}
                      errors={errors.schedules}
                    />
                  ))}
                </div>
              </CardContent>
            </Card>
          </section>

          <section className="w-full max-w-none mt-6">
            <Card className="bg-white border-gray-100 shadow-sm w-full">
              <CardHeader>
                <CardTitle className="text-title3-semibold font-sf-pro-text text-label-primary">
                  Foto
                </CardTitle>
              </CardHeader>
              <CardContent>
                <FormField name="foto">
                  {({ field }) => (
                    <FormItem className="flex flex-col">
                      <FormControl>
                        <Label
                          htmlFor="foto-upload"
                          className="flex flex-col items-center justify-center w-full h-65 bg-[#eef0f3] rounded-2xl cursor-pointer hover:bg-[#e6e9ec]"
                        >
                          <div className="flex flex-col items-center justify-center text-gray-500">
                            <Camera className="w-5 h-5 mb-2" />
                            <p className="mb-1 text-sm">
                              Clique para adicionar uma foto
                            </p>
                          </div>
                          <Input
                            id="foto-upload"
                            type="file"
                            className="hidden"
                            {...field}
                          />
                        </Label>
                      </FormControl>
                      <FormMessage name="foto" />
                    </FormItem>
                  )}
                </FormField>
              </CardContent>
            </Card>
          </section>

          <div className="w-full mt-6 flex justify-end">
            <Button
              type="submit"
              disabled={isSubmitting}
              variant="purple"
              size="lg"
              className="mt-6 text-white cursor-pointer"
            >
              {isSubmitting
                ? 'Salvando...'
                : isEditing
                  ? 'Atualizar Iniciativa'
                  : 'Salvar Iniciativa'}
            </Button>
          </div>
        </Form>
      </main>
    </div>
  )
}
