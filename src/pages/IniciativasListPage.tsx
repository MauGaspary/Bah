import {
    Pagination,
    PaginationContent,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
  } from "@/components/ui/pagination"


import IniciativasSearchbar from '@/components/ui/IniciativasSearchbar'
import IniciativasList from '@/components/ui/IniciativasList/IniciativasList'

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

                <div className="mt-16">
                <IniciativasList />
                </div>


                <div className="mt-3">
                <Pagination>
                    <PaginationContent>
                        <PaginationItem>
                        <PaginationPrevious href="#" />
                        </PaginationItem>

                        <PaginationItem>
                        <PaginationLink href="#">1</PaginationLink>
                        </PaginationItem>

                        <PaginationItem>
                        <PaginationLink href="#">2</PaginationLink>
                        </PaginationItem>

                        <PaginationItem>
                        <PaginationLink href="#">3</PaginationLink>
                        </PaginationItem>

                        <PaginationItem>
                        <PaginationNext href="#" />
                        </PaginationItem>
                    </PaginationContent>
                </Pagination>
  
                </div>
            </div>

        

        </div>
    </div>

    
  )
}

export default IniciativasListPage