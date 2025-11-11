import { FaFacebook, FaInstagram, FaLinkedin, FaYoutube } from 'react-icons/fa'
import { FaMapMarkerAlt, FaEnvelope, FaPhoneAlt } from 'react-icons/fa'
import { useNavigate } from 'react-router-dom'

const Footer = () => {
  const currentYear = new Date().getFullYear()
  const navigate = useNavigate()

  const handleNavigation = (sectionId: string) => {
    const scrollToSection = () => {
      const el = document.getElementById(sectionId)
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }

    if (window.location.pathname !== '/') {
      navigate('/', { state: { scrollTo: sectionId } })
    } else {
      scrollToSection()
    }
  }

  return (
    <footer className="bg-bah-purple text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div>
            <h3 className="text-white font-bold text-lg mb-4">Sobre o BAH</h3>
            <p className="text-sm leading-relaxed">
              Somos uma Plataforma de Inovação de Caxias do Sul que pensa de
              forma aberta, integrada e colaborativa.
            </p>
          </div>

          <div>
            <h3 className="text-white font-bold text-lg mb-4">Links Rápidos</h3>
            <ul className="space-y-2">
              <li>
                <button
                  onClick={() => handleNavigation('about-section')}
                  className="text-sm hover:text-[#c7d871] transition-colors text-left"
                >
                  Sobre Nós
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleNavigation('values-section')}
                  className="text-sm hover:text-[#c7d871] transition-colors text-left"
                >
                  Nossos Valores
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleNavigation('journey-section')}
                  className="text-sm hover:text-[#c7d871] transition-colors text-left"
                >
                  Jornada
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleNavigation('contact-section')}
                  className="text-sm hover:text-[#c7d871] transition-colors text-left"
                >
                  Contato
                </button>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-bold text-lg mb-4">Contato</h3>
            <ul className="space-y-3">
              <li className="flex items-start space-x-2">
                <FaMapMarkerAlt className="text-[#c7d871] mt-1 flex-shrink-0" />
                <span className="text-sm">R. não sei, Porto Alegre - RS</span>
              </li>
              <li className="flex items-center space-x-2">
                <FaEnvelope className="text-[#c7d871] flex-shrink-0" />
                <a
                  href="mailto:contato@buracoadao.com.br"
                  className="text-sm hover:text-[#c7d871] transition-colors"
                >
                  contato@bah.com.br
                </a>
              </li>
              <li className="flex items-center space-x-2">
                <FaPhoneAlt className="text-[#c7d871] flex-shrink-0" />
                <a
                  href="tel:+555133086464"
                  className="text-sm hover:text-[#c7d871] transition-colors"
                >
                  (51) 3308-6464
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-bold text-lg mb-4">Redes Sociais</h3>
            <div className="flex space-x-4">
              <a
                href="https://facebook.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-2xl hover:text-[#c7d871] transition-colors"
                aria-label="Facebook"
              >
                <FaFacebook />
              </a>
              <a
                href="https://instagram.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-2xl hover:text-[#c7d871] transition-colors"
                aria-label="Instagram"
              >
                <FaInstagram />
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-2xl hover:text-[#c7d871] transition-colors"
                aria-label="LinkedIn"
              >
                <FaLinkedin />
              </a>
              <a
                href="https://youtube.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-2xl hover:text-[#c7d871] transition-colors"
                aria-label="YouTube"
              >
                <FaYoutube />
              </a>
            </div>
            <p className="text-sm mt-6">
              Siga-nos nas redes sociais e fique por dentro das novidades!
            </p>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-gray-400">
              © {currentYear} BAH Plataforma de Inovação de Caxias do Sul.
              Todos os direitos reservados.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a
                href="/politica-privacidade"
                className="text-sm text-gray-400 hover:text-[#c7d871] transition-colors"
              >
                Política de Privacidade
              </a>
              <a
                href="/termos-uso"
                className="text-sm text-gray-400 hover:text-[#c7d871] transition-colors"
              >
                Termos de Uso
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
