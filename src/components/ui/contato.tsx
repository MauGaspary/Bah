import React from 'react'
import {
  FaMapMarkerAlt,
  FaEnvelope,
  FaPhoneAlt,
  FaFacebook,
  FaInstagram,
  FaLinkedin,
  FaYoutube,
} from 'react-icons/fa'

import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import type {
  ContactFormState,
  ContactInfoItemProps,
  SocialMediaLinkProps,
} from '@/interfaces/interfaceContato'

const ContactInfoItem: React.FC<ContactInfoItemProps> = ({
  icon,
  title,
  content,
}) => (
  <div className="flex items-start space-x-3 mb-6">
    <div className="text-2xl mt-1" style={{ color: '#c7d871' }}>
      {icon}
    </div>
    <div>
      <h4 className="font-bold text-gray-800">{title}</h4>
      <p className="text-sm text-gray-600">{content}</p>
    </div>
  </div>
)

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

      <Button type="submit" className="bg-[#542E82] hover:bg-purple-800">
        Enviar mensagem
      </Button>
    </form>
  )
}

// Componente de link de redes sociais
const SocialMediaLink: React.FC<SocialMediaLinkProps> = ({
  icon,
  href,
  color,
}) => (
  <a
    href={href}
    target="_blank"
    rel="noopener noreferrer"
    className={`text-white p-3 rounded-full shadow-lg hover:opacity-80 transition duration-300 ease-in-out ${color}`}
  >
    {icon}
  </a>
)

// Componente principal Contato
const Contato: React.FC = () => {
  return (
    <div className="min-h-screen container mx-auto px-4 pb-16 md:pt-4">
      {/* Título e Subtítulo */}
      <header className="text-center mb-8">
        <h1 className="text-5xl font-extrabold text-gray-900 mb-2">
          Contato
          <span className="block w-[120px] h-[5px] bg-[#c7d871] mx-auto mt-2 rounded-full"></span>
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Entre em contato conosco para mais informações sobre o ecossistema de
          inovação
        </p>
      </header>

      <main className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:items-center">
        {/* Formulário */}
        <div className="lg:col-span-1">
          <ContactForm />
        </div>

        <div className="lg:col-span-1 flex flex-col justify-center lg:ml-16">
          <ContactInfoItem
            icon={<FaMapMarkerAlt />}
            title="Endereço"
            content="Rua Sinimbu, 1670, Caxias do Sul - RS"
          />
          <ContactInfoItem
            icon={<FaEnvelope />}
            title="Email"
            content="contato@bah3.com.br"
          />
          <ContactInfoItem
            icon={<FaPhoneAlt />}
            title="Telefone"
            content="(54) 3218-8000"
          />
        </div>
      </main>

      {/* Redes Sociais */}
      <section className="text-center mt-16">
        <h3 className="text-xl font-bold text-gray-800 mb-6">
          Redes Sociais
          <span className="block w-[120px] h-[3px] bg-[#c7d871] mx-auto mt-2 rounded-full"></span>
        </h3>
        <div className="flex justify-center space-x-4 text-3xl">
          <SocialMediaLink icon={<FaFacebook />} href="#" color="bg-blue-600" />
          <SocialMediaLink
            icon={<FaInstagram />}
            href="#"
            color="bg-pink-600"
          />
          <SocialMediaLink icon={<FaLinkedin />} href="#" color="bg-blue-700" />
          <SocialMediaLink icon={<FaYoutube />} href="#" color="bg-red-600" />
        </div>
      </section>
    </div>
  )
}

export default Contato
