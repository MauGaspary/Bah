import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '../pagination'

import { useState, useEffect } from 'react'
import ListItem from './ListItem'
import ConfirmModal from '../ConfirmModal'

import type {
  User,
  UsersListProps,
} from '@/interfaces/IUsers'

import { fetchUsers, deleteUser } from '@/service/users'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

{/*

const mockUsuarios = Array.from({ length: 22 }).map((_, i) => ({
  id: i + 1,
  title: `Usuário ${i + 1}`,
  description: 'usuario@email.com',
  imageUrl: 'https://placehold.co/150x150.png?text=',
}))

*/}

function UsuariosList({searchQuery}: UsersListProps) {
  const [currentPage, setCurrentPage] = useState(1)
  const [deletingId, setDeletingId] = useState<string | null>(null)
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
  const [userToDelete, setUserToDelete] = useState<User | null>(null)

  const queryClient = useQueryClient()
  const itemsPerPage = 5

  const {
    data: usuariosData,
    isLoading: loading,
    error,
  } = useQuery({
    queryKey: ['usuarios', searchQuery, currentPage, itemsPerPage],
    queryFn: () => fetchUsers(searchQuery, currentPage, itemsPerPage),
  })

  const usuarios = usuariosData?.items || []
  const total = usuariosData?.total || 0
  const totalPages = Math.max(1, Math.ceil(total / itemsPerPage))

  const deleteMutation = useMutation({
    mutationFn: deleteUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['usuarios'] })
      closeDeleteConfirm()
    },
    onError: () => {
      console.error('Erro ao excluir usuário')
    },
    onSettled: () => {
      setDeletingId(null)
    },
  })

  const openDeleteConfirm = (user: User) => {
    setUserToDelete(user)
    setIsDeleteModalOpen(true)
  }

  const closeDeleteConfirm = () => {
    setUserToDelete(null)
    setIsDeleteModalOpen(false)
  }

  useEffect(() => {
    // Reset to first page when search changes
    setCurrentPage(1)
  }, [searchQuery])

  const handleConfirmDelete = async () => {
    if (!userToDelete) return

    const { id } = userToDelete
    setDeletingId(id)
    deleteMutation.mutate(id)
  }

  return (
    <div>
      <div className="rounded-card bg-white shadow-md  overflow-hidden">
        <div className="bg-bah-purple px-6 py-6">
          <div className="flex justify-between items-end">
            <h1 className="text-title3-regular font-mulish text-white self-center">
              Usuários Cadastrados
            </h1>
            <p className="text-body-regular font-mulish text-white">
                {total} usuários encontrados
            </p>
          </div>
        </div>

        <div className="flex px-6 py-2 bg-background-secondary justify-between">
          <h1 className="text-body-regular font-mulish">Usuário</h1>
          <h1 className="text-body-regular font-mulish mr-51">Ações</h1>
        </div>

        {!loading && error && (
          <div className="mt-4 space-y-2 text-body-regular text-center font-mulish">
            <p className="text-error">Erro ao carregar usuários</p>
          </div>
        )}

        <div className="space-y-3">
          {usuarios.map((item: User, index: number) => (
            <ListItem
              variant='usuario'
              key={item.id}
              title={item.nome}
              email={item.email}
              isLast={index === usuarios.length - 1}
              isDeleting={deletingId === item.id}
              onDelete={() => openDeleteConfirm(item)}
            />
          ))}
        </div>
      </div>
      <div className="py-8">
        <Pagination>
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious
                href="#"
                disabled={currentPage === 1}
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
                disabled={currentPage === totalPages}
                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>

      <ConfirmModal
        isOpen={isDeleteModalOpen}
        title="Excluir Usuário"
        message={`Tem certeza que deseja excluir o usuário "${userToDelete?.nome}"?`}
        confirmText="Excluir"
        cancelText="Cancelar"
        isLoading={deletingId === userToDelete?.id}
        onConfirm={handleConfirmDelete}
        onCancel={closeDeleteConfirm}
      />
    </div>
  )
}

export default UsuariosList