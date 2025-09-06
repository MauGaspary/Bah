import { zodResolver } from '@hookform/resolvers/zod'
import { Eye, EyeOff } from 'lucide-react'
import { X } from 'lucide-react'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { z } from 'zod'

import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Form, FormField, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useAuth } from '@/contexts/AuthContext'

function LoginAdminPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [rememberMe, setRememberMe] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { login } = useAuth()

  const loginSchema = z.object({
    email: z.string().email({ message: 'Email inválido' }),
    password: z.string().min(1, { message: 'Senha é obrigatória' }),
  })

  type LoginForm = z.infer<typeof loginSchema>

  const form = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  })

  const handleSubmit = async (values: LoginForm) => {
    setIsLoading(true)
    setError('')

    try {
      await login(values.email, values.password)
      navigate('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao fazer login')
    } finally {
      setIsLoading(false)
    }
  }

  const clearEmail = () => form.setValue('email', '')

  return (
    <div className="min-h-screen flex relative">
      <div
        className="absolute pointer-events-none select-none left-0 bottom-0 
             w-[200px] max-w-[14vw] min-w-[120px] opacity-95
             max-[1400px]:w-[140px] max-[1024px]:w-[100px]"
      >
        <img
          src="/src/assets/Bah Projeto Group 9.png"
          alt="Decorative Element"
          className="w-full h-auto"
        />
      </div>

      <div className="w-1/2 bg-white flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <h1 className="text-4xl font-bold text-bah-purple mb-2">Login</h1>
          <p className="text-gray-500 mb-8">
            Please fill your detail to access your account.
          </p>

          <Form
            form={form}
            onSubmit={handleSubmit}
            className="space-y-6"
            noValidate
          >
            <FormField name="email">
              {({ field }) => (
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="youremail@example.com"
                    required
                    {...field}
                    trailing={
                      field.value ? (
                        <span
                          role="button"
                          tabIndex={0}
                          onClick={clearEmail}
                          onKeyDown={e => {
                            if (e.key === 'Enter' || e.key === ' ') clearEmail()
                          }}
                          className="w-6 h-6 flex items-center justify-center cursor-pointer text-gray-500 hover:text-gray-700"
                          aria-label="Limpar email"
                        >
                          <X className="w-4 h-4" />
                        </span>
                      ) : null
                    }
                  />
                  <FormMessage name="email" />
                </div>
              )}
            </FormField>

            <FormField name="password">
              {({ field }) => (
                <div>
                  <Label htmlFor="password">Password</Label>
                  <Input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    {...field}
                    trailing={
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="w-5 h-5 text-gray-500 hover:text-gray-700 cursor-pointer"
                        aria-label={
                          showPassword ? 'Hide password' : 'Show password'
                        }
                      >
                        {showPassword ? (
                          <EyeOff className="w-5 h-5" />
                        ) : (
                          <Eye className="w-5 h-5" />
                        )}
                      </button>
                    }
                  />
                  <FormMessage name="password" />
                </div>
              )}
            </FormField>

            <div className="flex items-center justify-between">
              <Checkbox
                checked={rememberMe}
                onChange={e =>
                  setRememberMe((e.target as HTMLInputElement).checked)
                }
                label="Remember Me"
              />
            </div>

            {error && (
              <div className="text-red-500 text-sm text-center bg-red-50 p-3 rounded-lg">
                {error}
              </div>
            )}

            <Button
              type="submit"
              variant="purple"
              size="default"
              className="w-full cursor-pointer"
              disabled={isLoading}
            >
              {isLoading ? 'Signing in...' : 'Sign in'}
            </Button>
          </Form>
        </div>
      </div>

      <div className="w-1/2 bg-bah-purple flex items-center justify-center">
        <div className="text-center">
          <div className="mb-6">
            <img
              src="/src/assets/Bah Projeto Group 4.png"
              alt="BAH Logo"
              className="w-72 h-auto mx-auto"
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoginAdminPage
