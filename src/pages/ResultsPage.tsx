import Header from '@/components/ui/Header/Header'
import CardItem from '@/components/ui/CardItem'

function ResultsPage() {
    return (
        <div>
            <Header variant="default" />
            <main className="min-h-screen bg-white py-8">
                <div className="container mx-auto px-4 max-w-4xl">
                    <div className="flex flex-col gap-4 pt-20">
                     <CardItem 
                        imageUrl="https://placehold.co/150x150.png?text=Initiative" 
                        title="Iniciativa 1 " 
                        description="Descrição da iniciativa 1" 
                        hora_inicio="17:30:00.573Z"
                        hora_fim="19:30:00.573Z"
                     />

                     <CardItem 
                        imageUrl="https://placehold.co/150x150.png?text=Initiative" 
                        title="Iniciativa 1 " 
                        description="Descrição da iniciativa 1" 
                        hora_inicio="17:30:00.573Z"
                        hora_fim="19:30:00.573Z"
                     />

                     <CardItem 
                        imageUrl="https://placehold.co/150x150.png?text=Initiative" 
                        title="Iniciativa 1 " 
                        description="Descrição da iniciativa 1" 
                        hora_inicio="17:30:00.573Z"
                        hora_fim="19:30:00.573Z"
                     />

                     <CardItem 
                        imageUrl="https://placehold.co/150x150.png?text=Initiative" 
                        title="Iniciativa 1 " 
                        description="Descrição da iniciativa 1" 
                        hora_inicio="17:30:00.573Z"
                        hora_fim="19:30:00.573Z"
                     />
                    </div>
                </div>
            </main>
        </div>
    )
}

export default ResultsPage