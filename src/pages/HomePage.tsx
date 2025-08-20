import { Button } from '@/components/ui/button'
import { useNavigate } from 'react-router-dom'

function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-white flex items-center justify-center">
      <div className="text-center space-y-8">
        {/* Logo/Título */}
        <div className="space-y-4">
          <h1 className="text-large-title font-kanit text-label-primary">
            BAH
          </h1>
          <p className="text-body-regular font-sf-pro text-label-secondary max-w-md">
            Bem-vindo ao sistema BAH. Uma aplicação simples e intuitiva.
          </p>
        </div>

        {/* Botão principal */}
        <Button 
          variant="primary" 
          onClick={() => navigate('/dashboard')}
          className="px-8 py-3"
        >
          Acessar Sistema
        </Button>
      </div>
    </div>
  )
}

export default HomePage