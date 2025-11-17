import React from 'react'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import type {
  ContactFormState,
} from '@/interfaces/interfaceContato'

// Componente do formulário de contato
const ContactForm: React.FC = () => {
  const [formData, setFormData] = React.useState<ContactFormState>({
    nomeCompleto: '',
    email: '',
    assunto: '',
    mensagem: '',
  })

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Dados do formulário:', formData)
    alert('Mensagem enviada! (Simulação)')
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h3 className="text-xl font-bold text-gray-800 mb-6">
        Envie uma mensagem
      </h3>

      <Input
        id="nomeCompleto"
        placeholder="Nome completo"
        value={formData.nomeCompleto}
        onChange={handleChange}
        required
      />

      <Input
        type="email"
        id="email"
        placeholder="Email"
        value={formData.email}
        onChange={handleChange}
        required
      />

      <Input
        id="assunto"
        placeholder="Assunto"
        value={formData.assunto}
        onChange={handleChange}
      />

      <Textarea
        id="mensagem"
        placeholder="Mensagem"
        rows={6}
        value={formData.mensagem}
        onChange={handleChange}
        required
        className="resize-none"
      />

      <Button type="submit" className="bg-[#542E82] hover:bg-purple-800 block self-end justify-self-end">
        Enviar mensagem
      </Button>
    </form>
  )
}

// Componente principal Contato
const Contato: React.FC = () => {
  return (
    <div className="container mx-auto px-4">
      {/* Título e Subtítulo */}
      <header className="text-center mb-8">
        <h2 className="text-3xl md:text-4xl font-bold text-center">
          Contato
          <span className="block w-[120px] h-[5px] bg-[#c7d871] mx-auto mt-2 rounded-full"></span>
        </h2>
        <p className="mt-5 max-w-md mx-auto">
          Entre em contato conosco para mais informações sobre o ecossistema de
          inovação
        </p>
      </header>

      <main className="flex flex-row w-full gap-12 items-center justify-center">
        {/* Formulário */}
        <div className="w-full md:w-2/3">
          <ContactForm />
        </div>
      </main>
    </div>
  )
}

export default Contato
