import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState, useEffect } from 'react'

import ConfirmModal from '../ConfirmModal'
import ListItem from './ListItem'

import type {
  IniciativasListProps,
  Iniciativa,
} from '@/interfaces/IIniciativas'

import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'

import { fetchIniciativas, deleteIniciativa } from '@/service/iniciativas'

function IniciativasList({ searchQuery }: IniciativasListProps) {
  const [currentPage, setCurrentPage] = useState(1)
  const [deletingId, setDeletingId] = useState<number | null>(null)
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
  const [iniciativaToDelete, setIniciativaToDelete] =
    useState<Iniciativa | null>(null)

  const queryClient = useQueryClient()
  const itemsPerPage = 5

  // Query para buscar iniciativas
  const {
    data: iniciativasData,
    isLoading: loading,
    error,
  } = useQuery({
    queryKey: ['iniciativas', searchQuery, currentPage, itemsPerPage],
    queryFn: () => fetchIniciativas(searchQuery, currentPage, itemsPerPage),
  })

  const iniciativas = iniciativasData?.items || []
  const total = iniciativasData?.total || 0
  const totalPages = Math.max(1, Math.ceil(total / itemsPerPage))

  const deleteMutation = useMutation({
    mutationFn: deleteIniciativa,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['iniciativas'] })
      closeDeleteConfirm()
    },
    onError: () => {
      console.error('Erro ao excluir iniciativa')
    },
    onSettled: () => {
      setDeletingId(null)
    },
  })

  useEffect(() => {
    // Reset to first page when search changes
    setCurrentPage(1)
  }, [searchQuery])

  const openDeleteConfirm = (iniciativa: Iniciativa) => {
    setIsDeleteModalOpen(true)
    setIniciativaToDelete(iniciativa)
  }

  const closeDeleteConfirm = () => {
    setIsDeleteModalOpen(false)
    setIniciativaToDelete(null)
  }

  const handleConfirmDelete = async () => {
    if (!iniciativaToDelete) return

    const { id } = iniciativaToDelete
    setDeletingId(id)
    deleteMutation.mutate(id)
  }

  return (
    <div>
      <div className="rounded-card bg-white shadow-md overflow-hidden flex flex-col">
        <div className="bg-bah-purple px-6 py-6">
          <div className="flex justify-between items-end">
            <h1 className="text-medium-title font-mulish text-white self-center">
              Iniciativas Cadastradas
            </h1>
            <p className="text-body-regular font-mulish text-white">
              {total} iniciativas encontradas
            </p>
          </div>
        </div>

        <div className="flex px-6 py-2 bg-background-secondary justify-between">
          <h1 className="text-body-regular font-mulish">Iniciativa</h1>
          <h1 className="text-body-regular font-mulish mr-53.5">Ações</h1>
        </div>

        {!loading && error && (
          <div className="mt-4 space-y-2 text-body-regular text-center font-mulish">
            <p className="text-error">Erro ao carregar iniciativas</p>
          </div>
        )}

        <div className="pb-2 space-y-2 flex-1">
          {iniciativas.map((item: Iniciativa, index: number) => (
            <ListItem
              key={item.id}
              title={item.titulo}
              description={item.descricao}
              imageUrl={item.imagem_url}
              isLast={index === iniciativas.length - 1}
              isDeleting={deletingId === item.id}
              onEdit={() => console.warn('Editar iniciativa', item.id)}
              onDelete={() => openDeleteConfirm(item)}
            />
          ))}
        </div>
      </div>
      <div className="py-4 fixed bottom-0 right-0 left-[15%]">
        <div className="px-6">
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
                  onClick={() =>
                    setCurrentPage(p => Math.min(totalPages, p + 1))
                  }
                />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        </div>
      </div>

      <ConfirmModal
        isOpen={isDeleteModalOpen}
        title="Excluir Iniciativa"
        message={`Tem certeza que deseja excluir a iniciativa "${iniciativaToDelete?.titulo}"?`}
        confirmText="Excluir"
        cancelText="Cancelar"
        isLoading={deletingId === iniciativaToDelete?.id}
        onConfirm={handleConfirmDelete}
        onCancel={closeDeleteConfirm}
      />
    </div>
  )
}

export default IniciativasList
