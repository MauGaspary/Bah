import { useState, useEffect } from 'react'
import ListItem from './ListItem'
import ConfirmModal from '../ConfirmModal'

import type { User, UsersListProps } from '@/interfaces/IUsers'

import { fetchUsers, deleteUser } from '@/service/users'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import SimplePagination from '../PageList'

function UsuariosList({ searchQuery }: UsersListProps) {
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
              variant="usuario"
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
      <div className="py-4 fixed bottom-0 right-0 left-[15%]">
        <div className="py-8">
          <SimplePagination
            totalPages={totalPages}
            page={currentPage}
            setPage={setCurrentPage}
            wrapperClassName="py-4 fixed bottom-0 left-[15%] w-[85%]"
          />
        </div>
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
