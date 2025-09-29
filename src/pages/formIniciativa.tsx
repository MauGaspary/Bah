import React, { useEffect, useState, type KeyboardEvent } from 'react'
import { useForm, useFieldArray, Controller } from 'react-hook-form'
import type { Control } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import toast, { Toaster } from 'react-hot-toast'
import { Camera, Star } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import SidebarAdm from '@/components/ui/sidebar'

const Input = React.forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement>
>(({ className = '', ...props }, ref) => (
  <input
    className={`w-full ${className} focus:outline-none focus:ring-0 focus:border-gray-300`}
    ref={ref}
    {...props}
  />
))

const Textarea = React.forwardRef<
  HTMLTextAreaElement,
  React.TextareaHTMLAttributes<HTMLTextAreaElement>
>(({ className = '', ...props }, ref) => (
  <textarea
    className={`w-full ${className} focus:outline-none focus:ring-0 focus:border-gray-300`}
    ref={ref}
    {...props}
  />
))

const Label: React.FC<React.LabelHTMLAttributes<HTMLLabelElement>> = ({
  children,
  className = '',
  ...props
}) => (
  <label className={className} {...props}>
    {children}
  </label>
)

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
        <label className="block text-xs font-bold text-black mb-2">Dia</label>
        <select
          value={dayValue ?? ''}
          onChange={e => onDayChange(e.target.value)}
          className="w-full px-4 py-2 border-2 border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-0 focus:border-gray-300"
        >
          {DAY_OPTIONS.map(opt => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-xs font-bold text-black mb-2">
          Horário Início
        </label>
        <select
          value={startValue ?? ''}
          onChange={e => onStartChange(e.target.value)}
          className="w-full px-4 py-2 border-2 border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-0 focus:border-gray-300"
        >
          {HOUR_OPTIONS.map(opt => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-xs font-bold text-black mb-2">
          Horário Fim
        </label>
        <select
          value={endValue ?? ''}
          onChange={e => onEndChange(e.target.value)}
          className="w-full px-4 py-2 border-2 border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-0 focus:border-gray-300"
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
  isAtivo: z.boolean(),
  tags: z.array(z.string()).min(1, 'Adicione pelo menos uma tag.'),
  schedules: z.array(scheduleSchema),
  newTag: z.string().optional(),
  foto: z.any().optional(),
})

type InitiativeFormData = z.infer<typeof initiativeSchema>

const ScheduleItem: React.FC<{
  index: number
  control: Control<InitiativeFormData>
  onRemove: (index: number) => void
  errors?: any
}> = ({ index, control, onRemove, errors }) => {
  return (
    <div className="bg-gray-50 rounded-[1rem] p-4 border border-gray-100 flex flex-col gap-3 mb-6">
      <div className="flex justify-between items-start">
        <div className="text-sm font-semibold">Horário {index + 1}</div>

        <Button
          type="button"
          onClick={() => onRemove(index)}
          className="text-red-500 hover:text-red-700 px-3 py-1 hover:bg-red-50 transition"
          aria-label={`Remover horário ${index + 1}`}
          variant="ghost"
          size="sm"
          style={{ borderRadius: '10px' }}
        >
          Remover
        </Button>
      </div>

      <div>
        <Controller
          name={`schedules.${index}.dia` as const}
          control={control}
          render={({ field: dayField }) => (
            <Controller
              name={`schedules.${index}.inicio` as const}
              control={control}
              render={({ field: inicioField }) => (
                <Controller
                  name={`schedules.${index}.fim` as const}
                  control={control}
                  render={({ field: fimField }) => (
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
                />
              )}
            />
          )}
        />
      </div>

      <div className="mt-2">
        <label className="block text-xs font-bold text-black mb-2">Tipo</label>
        <Controller
          name={`schedules.${index}.tipo` as const}
          control={control}
          render={({ field }) => (
            <select
              value={field.value ?? ''}
              onChange={field.onChange}
              className="w-full px-4 py-2 border-2 border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-0 focus:border-gray-300"
            >
              <option value="">Selecione o tipo</option>
              <option value="presencial">Presencial</option>
              <option value="online">Online</option>
              <option value="hibrido">Híbrido</option>
            </select>
          )}
        />
        {errors?.[index]?.tipo && (
          <p className="text-red-500 text-xs mt-1">
            {errors[index].tipo.message}
          </p>
        )}
      </div>
    </div>
  )
}

export default function FormIniciativa() {
  const [isEditing, setIsEditing] = useState(false)

  const {
    register,
    handleSubmit,
    control,
    reset,
    getValues,
    setValue,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<InitiativeFormData>({
    resolver: zodResolver(initiativeSchema),
    defaultValues: {
      titulo: '',
      local: '',
      link1: '',
      link2: '',
      organizador: '',
      descricao: '',
      isAtivo: false,
      tags: [],
      schedules: [],
      newTag: '',
      foto: undefined,
    },
  })

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

  const onSubmit = (data: InitiativeFormData) => {
    const fotoFileList = data.foto as unknown as FileList | undefined | null
    const foto =
      fotoFileList && fotoFileList.length > 0 ? fotoFileList[0] : undefined
    const { newTag, ...payload } = data
    console.log('Payload submetido:', { ...payload, foto })
    toast.success(
      isEditing
        ? 'Iniciativa atualizada com sucesso!'
        : 'Iniciativa criada com sucesso!'
    )
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
        isAtivo: false,
        tags: [],
        schedules: [],
        newTag: '',
        foto: undefined,
      })
    }
  }, [isEditing, reset])

  return (
    <div className="flex">
      <SidebarAdm />
      <main className="p-6 min-h-screen bg-gray-50">
        <Toaster position="top-right" reverseOrder={false} />

        <header className="mb-6 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-mulish text-[#5a2d86]">
              {isEditing ? 'Editar Iniciativa' : 'Criar Iniciativa'}
            </h1>
            <p className="text-sm text-gray-600">
              {isEditing ? 'Editar a iniciativa' : 'Criar nova iniciativa'}
            </p>
          </div>
          <Button
            type="button"
            onClick={() => setIsEditing(!isEditing)}
            className="bg-gray-200 text-black px-4 py-1 hover:bg-gray-300"
            style={{
              borderRadius: '10px',
              minWidth: 'fit-content',
              height: '2.5rem',
            }}
          >
            {isEditing ? 'Cancelar Edição' : 'Editar'}
          </Button>
        </header>

        <form onSubmit={handleSubmit(onSubmit)}>
          <section className="w-full">
            <div className="relative bg-white rounded-[1.5rem] p-6 border border-gray-100 shadow-sm w-full">
              <div className="flex justify-between items-center mb-6">
                <h2 className="font-mulish text-lg font-bold text-black">
                  Detalhes da Iniciativa
                </h2>
                <div className="flex items-center gap-2">
                  <Star
                    className={`w-5 h-5 ${watch('isAtivo') ? 'text-black' : 'text-gray-400'}`}
                  />
                  <Controller
                    name="isAtivo"
                    control={control}
                    render={({ field }) => (
                      <Switch
                        checked={field.value}
                        onCheckedChange={field.onChange}
                        className={`
    relative inline-flex h-6 w-11 items-center rounded-full 
    ${field.value ? 'bg-green-500' : 'bg-gray-300'}
    transition-colors
  `}
                      >
                        <span
                          className={`
      pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white
      transition-transform duration-200 ease-in-out
      ${field.value ? 'translate-x-6' : 'translate-x-1'}
    `}
                        />
                      </Switch>
                    )}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-black mb-2">
                      Título
                    </label>
                    <Input
                      {...register('titulo')}
                      placeholder="Digite o título"
                      className="px-4 py-2 border-2 border-gray-200 rounded-[0.8rem] text-sm placeholder:text-gray-400"
                    />
                    {errors.titulo && (
                      <p className="text-red-500 text-xs mt-1">
                        {errors.titulo.message}
                      </p>
                    )}
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-black mb-2">
                      Local
                    </label>
                    <Input
                      {...register('local')}
                      placeholder="Digite o local"
                      className="px-4 py-2 border-2 border-gray-200 rounded-[0.8rem] text-sm placeholder:text-gray-400"
                    />
                    {errors.local && (
                      <p className="text-red-500 text-xs mt-1">
                        {errors.local.message}
                      </p>
                    )}
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-black mb-2">
                      Link 1
                    </label>
                    <Input
                      {...register('link1')}
                      placeholder="https://exemplo.com"
                      className="px-4 py-2 border-2 border-gray-200 rounded-[0.8rem] text-sm placeholder:text-gray-400"
                    />
                    {errors.link1 && (
                      <p className="text-red-500 text-xs mt-1">
                        {errors.link1.message}
                      </p>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="md:col-span-2">
                    <label className="block text-xs font-bold text-black mb-2">
                      Link 2
                    </label>
                    <Input
                      {...register('link2')}
                      placeholder="https://linkedin.com/exemplo"
                      className="px-4 py-2 border-2 border-gray-200 rounded-[0.8rem] text-sm placeholder:text-gray-400"
                    />
                    {errors.link2 && (
                      <p className="text-red-500 text-xs mt-1">
                        {errors.link2.message}
                      </p>
                    )}
                  </div>
                  <div className="md:col-span-1">
                    <label className="block text-xs font-bold text-black mb-2">
                      Organizador
                    </label>
                    <select
                      {...register('organizador')}
                      className={`w-full px-4 py-2 border-2 border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-0 focus:border-gray-300 ${!organizadorValue ? 'text-gray-400' : 'text-black'}`}
                    >
                      <option value="" disabled>
                        Selecione
                      </option>
                      <option value="Equipe BAH">Equipe BAH</option>
                    </select>
                    {errors.organizador && (
                      <p className="text-red-500 text-xs mt-1">
                        {errors.organizador.message}
                      </p>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="md:col-span-2">
                    <label className="block text-xs font-bold text-black mb-2">
                      Descrição
                    </label>
                    <Textarea
                      {...register('descricao')}
                      placeholder="Digite a descrição"
                      className="px-4 py-3 border-2 border-gray-200 rounded-[0.8rem] text-sm h-28 resize-y placeholder:text-gray-400"
                    />
                    {errors.descricao && (
                      <p className="text-red-500 text-xs mt-1">
                        {errors.descricao.message}
                      </p>
                    )}
                  </div>

                  <div className="md:col-span-1">
                    <label className="block text-xs font-bold text-black mb-2">
                      Tags
                    </label>
                    <div className="w-full border-2 border-gray-200 rounded-[1rem] min-h-[7rem] p-3 flex flex-col">
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
                              className="text-lime-400 hover:text-lime-600 hover:ring-0 focus:ring-0 focus:outline-none"
                              aria-label={`Remover tag ${getValues(`tags.${index}`)}`}
                              variant="ghost"
                              size="sm"
                            >
                              ✕
                            </Button>
                          </span>
                        ))}
                      </div>
                      <Input
                        {...register('newTag')}
                        onKeyDown={handleNewTagKeyDown}
                        placeholder="Adicionar tag..."
                        className="w-full mt-auto pt-2 border-t border-gray-200 text-sm focus:outline-none bg-transparent placeholder:text-gray-400"
                      />
                    </div>
                    {errors.tags && (
                      <p className="text-red-500 text-xs mt-1">
                        {errors.tags.message}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section className="w-full mt-8">
            <div className="bg-white rounded-[1.5rem] p-6 border border-gray-100 shadow-sm w-full">
              <div className="flex justify-between items-center mb-6">
                <h2 className="font-mulish text-lg font-bold text-black">
                  Horários
                </h2>

                <div className="flex flex-col items-center">
                  <p className="text-xs font-bold mb-1">
                    Clique para adicionar
                  </p>
                  <Button
                    type="button"
                    onClick={() =>
                      appendSchedule({ dia: '', inicio: '', fim: '', tipo: '' })
                    }
                    className="bg-[#f2f2f7] text-[#85858b] hover:bg-gray-300 flex items-center justify-center"
                    style={{
                      width: '35px',
                      minWidth: '50px',
                      maxWidth: '50px',
                      height: '20px',
                      borderRadius: '10px',
                      padding: 0,
                      boxSizing: 'border-box',
                    }}
                    aria-label="Adicionar horário"
                  >
                    +
                  </Button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-h-[520px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-gray-300">
                {scheduleFields.length === 0 && (
                  <div className="col-span-full text-sm text-gray-500">
                    Nenhum horário adicionado — clique em + para adicionar.
                  </div>
                )}

                {scheduleFields.map((field, index) => (
                  <ScheduleItem
                    key={field.id}
                    index={index}
                    control={control}
                    onRemove={removeSchedule}
                    errors={errors.schedules}
                  />
                ))}
              </div>
            </div>
          </section>

          <section className="bg-white rounded-[1.5rem] p-6 border border-gray-100 shadow-sm w-full mt-6">
            <h2 className="font-mulish text-lg font-bold text-black mb-6">
              Foto
            </h2>

            <Label
              htmlFor="foto-upload"
              className="flex flex-col items-center justify-center w-full h-65 bg-[#eef0f3] rounded-2xl cursor-pointer hover:bg-[#e6e9ec]"
            >
              <div className="flex flex-col items-center justify-center text-gray-500">
                <Camera className="w-5 h-5 mb-2" />
                <p className="mb-1 text-sm">Clique para adicionar uma foto</p>
              </div>
              <Input
                id="foto-upload"
                type="file"
                className="hidden"
                {...register('foto')}
              />
            </Label>

            {errors.foto && (
              <p className="text-red-500 text-xs mt-2">
                {(errors.foto as any).message}
              </p>
            )}
          </section>

          <div className="mt-6 flex justify-start">
            <Button
              type="submit"
              disabled={isSubmitting}
              className={`bg-[#5a2d86] text-white hover:bg-[#4a246d] mt-6 rounded-lg h-12 px-6 ${isSubmitting ? 'opacity-70 cursor-not-allowed' : ''}`}
            >
              {isSubmitting
                ? 'Salvando...'
                : isEditing
                  ? 'Atualizar Iniciativa'
                  : 'Salvar Iniciativa'}
            </Button>
          </div>
        </form>
      </main>
    </div>
  )
}
