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

interface ContactFormState {
  nomeCompleto: string
  email: string
  assunto: string
  mensagem: string
}

interface ContactInfoItemProps {
  icon: React.ReactNode
  title: string
  content: string
}

const ContactInfoItem: React.FC<ContactInfoItemProps> = ({
  icon,
  title,
  content,
}) => (
  <div className="flex items-start space-x-3 mb-6">
    <div className="text-lime-600 text-2xl mt-1">{icon}</div>
    <div>
      <h4 className="font-bold text-gray-800">{title}</h4>
      <p className="text-sm text-gray-600">{content}</p>
    </div>
  </div>
)

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
    // Lógica de envio do formulário aqui
    console.log('Dados do formulário:', formData)
    alert('Mensagem enviada! (Simulação)')
  }

  const inputClasses =
    'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-lime-500 transition duration-150 ease-in-out'

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h3 className="text-xl font-bold text-gray-800 mb-6">
        Envie uma mensagem
      </h3>

      <div>
        <input
          type="text"
          id="nomeCompleto"
          placeholder="Nome completo"
          value={formData.nomeCompleto}
          onChange={handleChange}
          className={inputClasses}
          required
        />
      </div>

      <div>
        <input
          type="email"
          id="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          className={inputClasses}
          required
        />
      </div>

      <div>
        <input
          type="text"
          id="assunto"
          placeholder="Assunto"
          value={formData.assunto}
          onChange={handleChange}
          className={inputClasses}
        />
      </div>

      <div>
        <textarea
          id="mensagem"
          placeholder="Mensagem"
          rows={6}
          value={formData.mensagem}
          onChange={handleChange}
          className={`${inputClasses} resize-none`}
          required
        />
      </div>

      <button
        type="submit"
        className="w-48 py-3 px-6 bg-[#542E82] text-white font-semibold rounded-full shadow-md hover:bg-purple-800 transition duration-300 ease-in-out"
      >
        Enviar mensagem
      </button>
    </form>
  )
}

// Componente de Redes Sociais
interface SocialMediaLinkProps {
  icon: React.ReactNode
  href: string
  color: string
}

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

const Contato: React.FC = () => {
  return (
    <div className="min-h-screen bg-white py-12">
      <div className="container mx-auto px-4 max-w-6xl">
        {/* Título e Subtítulo */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-extrabold text-gray-900 mb-2">
            Contato
            <span className="block w-[120px] h-[5px] bg-[#c7d871] mx-auto mt-2 rounded-full"></span>
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Entre em contato conosco para mais informações sobre o ecossistema
            de inovação
          </p>
        </header>

        <main className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div className="lg:col-span-1">
            <ContactForm />
          </div>

          <div className="lg:col-span-1 lg:mt-12">
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

        <section className="text-center mt-20">
          <h3 className="text-xl font-bold text-gray-800 mb-6">
            Redes Sociais
            <span className="block w-[120px] h-[3px] bg-[#c7d871] mx-auto mt-2 rounded-full"></span>
          </h3>
          <div className="flex justify-center space-x-4 text-3xl">
            <SocialMediaLink
              icon={<FaFacebook />}
              href="#"
              color="bg-blue-600"
            />
            <SocialMediaLink
              icon={<FaInstagram />}
              href="#"
              color="bg-pink-600"
            />
            <SocialMediaLink
              icon={<FaLinkedin />}
              href="#"
              color="bg-blue-700"
            />
            <SocialMediaLink icon={<FaYoutube />} href="#" color="bg-red-600" />
          </div>
        </section>
      </div>
    </div>
  )
}

export default Contato
