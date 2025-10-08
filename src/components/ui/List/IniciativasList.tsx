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

interface Iniciativa{
  id: number;
  title: string;
  description: string;
  imageUrl: string;
}

function IniciativasList() {
  const [iniciativas, setIniciativas] = useState<Iniciativa[]>([]);
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
        const response = await api.get<Iniciativa[]>("/admin/iniciativas");
        setIniciativas(response.data);
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
  }, []);

  if (loading) {
    return <p>Carregando...</p>;
  }
  if (error) {
    return <div>Erro ao carregar iniciativas</div>;
  }

  return (
    <div>
      <div className="rounded-card bg-white shadow-md overflow-hidden">
        <div className="bg-bah-purple px-6 py-6">
          <div className="flex justify-between items-end">
            <h1 className="text-medium-title font-mulish text-white self-center">
              Iniciativas Cadastradas
            </h1>
            <p className="text-body-regular font-mulish text-white">
              {iniciativas.length} iniciativas encontradas
            </p>
          </div>
        </div>

        <div className="flex px-6 py-2 bg-background-secondary justify-between">
          <h1 className="text-body-regular font-mulish">Iniciativa</h1>
          <h1 className="text-body-regular font-mulish mr-53.5">Ações</h1>
        </div>

        <div className="py-2 space-y-2 ">
          {currentItems.map((item, index) => (
            <ListItem
              key={item.id}
              title={item.title}
              description={item.description}
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

export default IniciativasList
