import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Camera, Star } from 'lucide-react'
import { useState } from 'react'
import { useForm, useFieldArray } from 'react-hook-form'
import toast, { Toaster } from 'react-hot-toast'
import { useNavigate } from 'react-router-dom'
import { z } from 'zod'

import type { IniciativaCreate } from '@/interfaces/IIniciativas'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import ScheduleItem from '@/components/ui/ScheduleItem'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import SidebarAdm from '@/components/ui/sidebar'
import { Switch } from '@/components/ui/switch'
import { Textarea } from '@/components/ui/textarea'
import { HorarioTipo } from '@/enums/HorarioTipo'
import { createIniciativa } from '@/service/iniciativas'
import { fetchOrganizadores } from '@/service/organizadores'
import { fetchTags } from '@/service/tags'

// Schema de validação para horários
const scheduleSchema = z.object({
  id: z.string().optional(),
  dia: z
    .string()
    .min(1, 'A data é obrigatória.')
    .regex(/^\d{4}-\d{2}-\d{2}$/, 'Formato de data inválido (YYYY-MM-DD)'),
  inicio: z.string().min(1, 'O horário de início é obrigatório.'),
  fim: z.string().min(1, 'O horário de fim é obrigatório.'),
  tipo: z.nativeEnum(HorarioTipo, {
    errorMap: () => ({ message: 'Tipo de horário inválido.' }),
  }),
})

// Schema de validação para o formulário principal
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
  foto: z.any().optional(),
})

type InitiativeFormData = z.infer<typeof initiativeSchema>

export default function FormIniciativa() {
  const [isEditing] = useState(false)
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const form = useForm<InitiativeFormData>({
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
      foto: undefined,
    },
  })

  const {
    control,
    watch,
    formState: { isSubmitting },
  } = form

  const {
    fields: scheduleFields,
    append: appendSchedule,
    remove: removeSchedule,
  } = useFieldArray({ control, name: 'schedules' })

  const {
    data: organizadores,
    isLoading: organizadoresLoading,
    isError: organizadoresError,
  } = useQuery({
    queryKey: ['organizadores'],
    queryFn: fetchOrganizadores,
  })

  const {
    data: tags,
    isLoading: tagsLoading,
    isError: tagsError,
  } = useQuery({
    queryKey: ['tags'],
    queryFn: fetchTags,
  })
  const createMutation = useMutation({
    mutationFn: createIniciativa,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['iniciativas'] })
      toast.success('Iniciativa criada com sucesso!')
      navigate('/admin/iniciativas')
    },
    onError: (error: Error) => {
      console.error('Erro ao criar iniciativa:', error)
      toast.error('Erro ao criar iniciativa')
    },
  })

  const onSubmit = (data: InitiativeFormData) => {
    if (isEditing) {
      // implementar patch depois
      toast.success('Iniciativa atualizada com sucesso!')
      return
    }

    const formatTimeToISO = (time: string): string => {
      return `${time}:00`
    }

    const iniciativaData: IniciativaCreate = {
      titulo: data.titulo,
      descricao: data.descricao,
      organizador_id: data.organizador,
      link: data.link1 || '',
      local: data.local,
      imagem_url:
        'https://mh1.com.br/wp-content/uploads/2024/10/luffy_capa.jpg', // ajustar imagens
      destaque: data.isAtivo,
      horarios: data.schedules.map(schedule => ({
        data_evento: schedule.dia,
        hora_inicio: formatTimeToISO(schedule.inicio),
        hora_fim: formatTimeToISO(schedule.fim),
        tipo: schedule.tipo as HorarioTipo,
      })),
      tag_ids: data.tags,
      descricoes_extras: [], //implementar depois
    }

    createMutation.mutate(iniciativaData)
  }

  return (
    <div className="flex h-screen w-full">
      <SidebarAdm />
      <main className="flex-1 p-6 bg-gray-50 overflow-y-auto w-full">
        <Toaster position="top-right" reverseOrder={false} />

        <header className="mb-6 flex justify-between items-center">
          <div>
            <h1 className="text-large-title font-kanit text-[#5a2d86]">
              {isEditing ? 'Editar Iniciativa' : 'Criar Iniciativa'}
            </h1>
            <p className="text-body-regular font-sf-pro text-label-secondary">
              {isEditing ? 'Editar a iniciativa' : 'Criar nova iniciativa'}
            </p>
          </div>
        </header>

        <Form form={form} onSubmit={onSubmit} className="w-full">
          {/* Seção: Detalhes da Iniciativa */}
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
                  {/* Primeira linha: Título, Local, Link 1 */}
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

                  {/* Segunda linha: Link 2, Organizador */}
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
                            <Select
                              value={field.value}
                              onValueChange={field.onChange}
                              disabled={
                                organizadoresLoading || organizadoresError
                              }
                            >
                              <SelectTrigger className="h-11 border px-4 border-gray-300 py-3 text-sm text-gray-400 focus-visible:ring-2 focus-visible:ring-bah-purple focus-visible:border-transparent data-[state=open]:ring-2 data-[state=open]:ring-bah-purple data-[state=open]:border-transparent shadow-none rounded-lg">
                                <SelectValue
                                  placeholder={
                                    organizadoresLoading
                                      ? 'Carregando...'
                                      : organizadoresError
                                        ? 'Erro ao carregar'
                                        : 'Selecione'
                                  }
                                />
                              </SelectTrigger>
                              <SelectContent className="border-bah-purple">
                                {organizadores?.map(org => (
                                  <SelectItem
                                    key={org.id}
                                    value={org.id}
                                    className="focus:bg-bah-purple focus:text-white"
                                  >
                                    {org.nome}
                                  </SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                          </FormControl>
                          <FormMessage name="organizador" />
                        </FormItem>
                      )}
                    </FormField>
                  </div>

                  {/* Terceira linha: Descrição e Tags */}
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
                      {({ field }) => (
                        <FormItem className="md:col-span-1 flex flex-col">
                          <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                            Tags
                          </FormLabel>
                          <FormControl>
                            <div className="w-full border-2 border-gray-200 rounded-[1rem] h-[10rem] p-3 flex flex-col">
                              <div className="flex-1 overflow-y-auto pr-1 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent">
                                {tagsLoading ? (
                                  <div className="text-sm text-gray-500">
                                    Carregando...
                                  </div>
                                ) : tagsError ? (
                                  <div className="text-sm text-red-500">
                                    Erro ao carregar tags
                                  </div>
                                ) : (
                                  <div className="grid grid-cols-1 gap-2">
                                    {tags?.map(t => {
                                      const checked = (
                                        field.value || []
                                      ).includes(t.id)
                                      return (
                                        <Checkbox
                                          key={t.id}
                                          checked={checked}
                                          onChange={e => {
                                            const isChecked = e.target.checked
                                            const current: string[] =
                                              field.value || []
                                            field.onChange(
                                              isChecked
                                                ? [...current, t.id]
                                                : current.filter(
                                                    id => id !== t.id
                                                  )
                                            )
                                          }}
                                          disabled={isSubmitting}
                                          label={t.nome}
                                        />
                                      )
                                    })}
                                  </div>
                                )}
                              </div>
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

          {/* Seção: Horários */}
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
                          tipo: HorarioTipo.PRESENCIAL,
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
                    />
                  ))}
                </div>
              </CardContent>
            </Card>
          </section>

          {/* Seção: Foto */}
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

          {/* Botão de Submit */}
          <div className="w-full mt-6 flex justify-start">
            <Button
              type="submit"
              disabled={isSubmitting || createMutation.isPending}
              variant="purple"
              size="lg"
              className="mt-6 text-white cursor-pointer"
            >
              {createMutation.isPending
                ? 'Criando...'
                : isSubmitting
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
