import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '../pagination'

import { useState } from 'react'
import ListItem from './ListItem'

const mockUsuarios = Array.from({ length: 22 }).map((_, i) => ({
  id: i + 1,
  title: `Usuário ${i + 1}`,
  description: 'usuario@email.com',
  imageUrl: 'https://placehold.co/150x150.png?text=',
}))

function UsuariosList() {
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 5

  const totalPages = Math.ceil(mockUsuarios.length / itemsPerPage)

  const startIndex = (currentPage - 1) * itemsPerPage
  const currentItems = mockUsuarios.slice(
      startIndex,
      startIndex + itemsPerPage
  )

  return (
    <div>
      <div className="rounded-card bg-white shadow-md  overflow-hidden">
        <div className="bg-bah-purple px-6 py-6">
          <div className="flex justify-between items-end">
            <h1 className="text-medium-title font-mulish text-white self-center">
              Usuários Cadastrados
            </h1>
            <p className="text-body-regular font-mulish text-white">
                {mockUsuarios.length} usuários encontrados
            </p>
          </div>
        </div>

        <div className="flex px-6 py-2 bg-background-secondary justify-between">
          <h1 className="text-body-regular font-mulish">Usuário</h1>
          <h1 className="text-body-regular font-mulish mr-53.5">Ações</h1>
        </div>

        <div className="py-2 space-y-2">
          {currentItems.map((item, index) => (
            <ListItem
              key={item.id}
              variant='usuario'
              title={item.title}
              email={item.description}
              imageUrl={item.imageUrl}
              isLast={index === currentItems.length - 1}
              onEdit={() => console.log("Editar")}
              onDelete={() => console.log("Excluir")}
            />
          ))}
        </div>
      </div>
      <div className="py-4">
        <Pagination>
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious
                href="#"
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
              />
            </PaginationItem>

            {[...Array(totalPages).keys()].map(i => (
              <PaginationItem key={i}>
                <PaginationLink
                  href="#"
                  isActive={currentPage === i + 1}
                  onClick={() => setCurrentPage(i + 1)}
                >
                  {i + 1}
                </PaginationLink>
              </PaginationItem>
            ))}

            <PaginationItem>
              <PaginationNext
                href="#"
                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  )
}

export default UsuariosList
