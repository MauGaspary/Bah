


import IniciativasSearchbar from '@/components/ui/IniciativasSearchbar'


function IniciativasListPage() {
  return ( 
    <div className="min-h-screen bg-background-secondary py-6 pr-6">
        <div className="ml-[20%] justify-start">
        <div className="text-left ">
          <h1 className="text-large-title font-mulish text-bah-purple ">
            Lista de Iniciativas
          </h1>
          <p className="text-body-regular font-mulish text-label-secondary">
            Gerencie todas iniciativas do sistema
          </p>
        </div>
            <div className="py-6 pr-6">
                <IniciativasSearchbar />
            </div>

            
        </div>
    </div>

    
  )
}

export default IniciativasListPage