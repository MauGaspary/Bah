import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useEffect, useRef } from 'react'
import { useForm } from 'react-hook-form'
import toast, { Toaster } from 'react-hot-toast'
import { useNavigate, useParams } from 'react-router-dom'
import { z } from 'zod'

import type {
  UserCreate,
  UserPatch,
  UserResponse,
} from '@/interfaces/IUsers'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import SidebarAdm from '@/components/ui/sidebar'
import {
  createUser,
  fetchUserById,
  patchUser,
} from '@/service/users'

// Schema de validação para o formulário principal
const usuarioSchema = z.object({
  nome: z.string().min(3, 'O nome deve ter pelo menos 3 caracteres.'),
  sobrenome: z.string().min(3, 'O sobrenome deve ter pelo menos 3 caracteres.'),
  email: z.string().email('O email deve ser válido.'),
  senha: z.string().min(6, 'A senha deve ter pelo menos 6 caracteres.'),
})

type UsuarioFormData = z.infer<typeof usuarioSchema>

export default function FormUsuario() {
  const navigate = useNavigate()
  const { id } = useParams()
  const isEditing = Boolean(id)
  const queryClient = useQueryClient()
  
  const objectUrlRef = useRef<string | null>(null)

  const form = useForm<UsuarioFormData>({
    resolver: zodResolver(usuarioSchema),
    defaultValues: {
      nome: '',
      sobrenome: '',
      email: '',
      senha: '',
    },
  })

  const {
    formState: { isSubmitting },
  } = form


  const { data: user } = useQuery({
    queryKey: ['usuario', id],
    queryFn: () => fetchUserById(id as string),
    enabled: isEditing,
  })
  const createMutation = useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['usuarios'] })
      toast.success('Usuário criado com sucesso!')
      navigate('/admin/usuarios')
    },
    onError: (error: Error) => {
      console.error('Erro ao criar usuário:', error)
      toast.error('Erro ao criar usuário')
    },
  })
  const patchMutation = useMutation({
    mutationFn: ({
      usuarioId,
      payload,
    }: {
      usuarioId: string
      payload: UserPatch
    }) => patchUser(usuarioId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['usuarios'] })
      toast.success('Usuário atualizado com sucesso!')
      navigate('/admin/usuarios')
    },
    onError: (error: Error) => {
      console.error('Erro ao atualizar usuário:', error)
      toast.error('Erro ao atualizar usuário')
    },
  })

  useEffect(() => {
    if (isEditing && user) {
      const usuario: UserResponse = user
      form.reset({
        nome: usuario.nome || '',
        sobrenome: usuario.sobrenome || '',
        email: usuario.email || '',
        senha: '',
      })
    }
  }, [isEditing, user, form])

  useEffect(() => {
    return () => {
      if (objectUrlRef.current) {
        URL.revokeObjectURL(objectUrlRef.current)
        objectUrlRef.current = null
      }
    }
  }, [])

  const onSubmit = (data: UsuarioFormData) => {
    if (isEditing && id && user) {
      
      const payload: UserPatch = {
        nome: user.nome, 
        sobrenome: user.sobrenome,
        email: user.email
      }

      patchMutation.mutate({ usuarioId: id, payload })
      return
    }

    const usuarioData: UserCreate = {
      nome: data.nome,
      sobrenome: data.sobrenome,
      email: data.email,
      id: '',
    }

    createMutation.mutate(usuarioData)
  }

  return (
    <div className="flex h-screen w-full">
      <SidebarAdm />
      <main className="flex-1 p-6 bg-gray-50 overflow-y-auto w-full relative">
        <Toaster position="top-right" reverseOrder={false} />

        <header className="mb-6 flex justify-between items-center">
          <div className="text-left">
            <h1 className="text-large-title font-mulish text-[#5a2d86]">
              {isEditing ? 'Editar Usuário' : 'Criar Usuário'}
            </h1>
            <p className="text-body-regular font-sf-pro text-label-secondary">
              {isEditing
                ? 'Edite seu usuario'
                : 'Crie aqui seu novo usuario'}
            </p>
          </div>
        </header>

        <Form form={form} onSubmit={onSubmit} className="w-full">
          {/* Seção: Detalhes do Usuário */}
          <section className="w-full max-w-none">
            <Card className="bg-white border-gray-100 shadow-sm w-full">
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle className="text-title3-semibold font-sf-pro-text text-label-primary">
                    Detalhes do Usuário
                  </CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 gap-4">
                  {/* Primeira linha: Nome, Sobrenome */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <FormField name="nome">
                      {({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                            Nome
                          </FormLabel>
                          <FormControl>
                            <Input
                              {...field}
                              placeholder="Digite o nome"
                              className="py-3 rounded-[0.8rem] text-sm placeholder:text-gray-400"
                            />
                          </FormControl>
                          <FormMessage name="nome" />
                        </FormItem>
                      )}
                    </FormField>

                    <FormField name="sobrenome">
                      {({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                            Sobrenome
                          </FormLabel>
                          <FormControl>
                            <Input
                              {...field}
                              placeholder="Digite o sobrenome"
                              className="py-3 rounded-[0.8rem] text-sm placeholder:text-gray-400"
                            />
                          </FormControl>
                          <FormMessage name="sobrenome" />
                        </FormItem>
                      )}
                    </FormField>

                  </div>

                  {/* Segunda linha: Email */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <FormField name="email">
                      {({ field }) => (
                        <FormItem className="md:col-span-2 flex flex-col">
                          <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                            Email
                          </FormLabel>
                          <FormControl>
                            <Input
                              {...field}
                              placeholder="Digite o email"
                              className="py-3 rounded-[0.8rem] text-sm placeholder:text-gray-400"
                            />
                          </FormControl>
                          <FormMessage name="email" />
                        </FormItem>
                      )}
                    </FormField>
                  </div>

                  {/* Terceira linha: Senha*/}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <FormField name="senha">
                      {({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel className="text-callout-semibold font-sf-pro-text text-label-primary mb-2">
                            Senha
                          </FormLabel>
                          <FormControl>
                            <Input
                              {...field}
                              placeholder="Digite a senha"
                              className="py-3 rounded-[0.8rem] text-sm placeholder:text-gray-400"
                              required
                              trailing={
                                <button
                                  type="button"
                                  className="w-5 h-5 text-gray-500 hover:text-gray-700 cursor-pointer" 
                                >
                                </button>
                              }
                            />
                          </FormControl>
                          <FormMessage name="senha" />
                        </FormItem>
                      )}
                    </FormField>
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>


          {/* Botão de Submit */}
          <div className="w-full mt-6 flex justify-end">
            <Button
              type="submit"
              disabled={
                isSubmitting ||
                createMutation.isPending ||
                patchMutation.isPending
              }
              variant="purple"
              size="lg"
              className="mt-6 text-white cursor-pointer"
            >
              {createMutation.isPending
                ? 'Criando...'
                : isSubmitting
                  ? 'Salvando...'
                  : isEditing
                    ? 'Atualizar Usuário'
                    : 'Salvar Usuário'}
            </Button>
          </div>
        </Form>
      </main>
    </div>
  )
}
