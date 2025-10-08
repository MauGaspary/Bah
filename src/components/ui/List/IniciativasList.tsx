import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'

import api from '@/service/api'
import { useState, useEffect } from 'react'
import ListItem from './ListItem'

interface IniciativasListProps{
  searchQuery: string;
}

interface Iniciativa{
  id: number;
  titulo: string;
  descricao: string;
  imagem_url: string;
}

interface IniciativasResponse{
  items: Iniciativa[];
  total: number;
}

function IniciativasList({searchQuery}: IniciativasListProps) {
  const [iniciativas, setIniciativas] = useState<Iniciativa[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string |  null>(null);
  const [currentPage, setCurrentPage] = useState (1);

  const itemsPerPage = 5;
  const totalPages = Math.ceil(iniciativas.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentItems = iniciativas.slice(startIndex, startIndex + itemsPerPage);

  useEffect(() => {
    async function fetchIniciativas() {
      try {
        const response = await api.get<IniciativasResponse>("/admin/iniciativas", {
          params: searchQuery ? { q: searchQuery } : {},
        })
        console.log(response);
        setIniciativas(response.data.items);
        setTotal(response.data.total);
      }
      catch (error) {
        console.error("Erro ao carregar iniciativas", error);
        setError("Erro ao carregar iniciativas");
      }
      finally {
        setLoading(false);
      }
    }
    fetchIniciativas();
  }, [searchQuery]);

  return (
    <div>
      <div className="rounded-card bg-white shadow-md overflow-hidden">
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

        <div className="mt-4 space-y-4 text-body-regular text-center font-mulish">
          {loading && <p className="text-label-secondary">Carregando iniciativas...</p>}

          {!loading && error && (
            <p className="text-error">{error}</p>
          )}

        </div>

        <div className="py-2 space-y-2 ">
          {currentItems.map((item, index) => (
            <ListItem
              key={item.id}
              title={item.titulo}
              description={item.descricao}
              imageUrl={item.imagem_url}
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

export default IniciativasList
