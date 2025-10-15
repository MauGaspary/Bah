import Header from '@/components/ui/Header/Header'
import CardItem from '@/components/ui/CardItem'

function ResultsPage() {
    return (
        <div>
            <Header variant="default" />
            <main className="min-h-screen bg-white py-8">
                <div className="container mx-auto px-4 max-w-4xl">
                    <div className="mt-20">
                     <CardItem 
                        imageUrl="https://placehold.co/150x150.png?text=Initiative" 
                        title="Iniciativa 1 " 
                        description="Descrição da iniciativa 1" 
                     />
                    </div>
                </div>
            </main>
        </div>
    )
}

export default ResultsPage