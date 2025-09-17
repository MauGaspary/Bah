
  
  import { useState } from "react";

  import UsuarioListItem from "./UsuarioListItem";

import {
    Pagination,
    PaginationContent,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
  } from "../pagination";

  
  const mockUsuarios = Array.from({ length: 22 }).map((_, i) => ({
    id: i + 1,
    title: "Usuário",
    description: "usuario@email.com",
    imageUrl: "https://placehold.co/150x150.png?text=",
  }));
  
  function UsuariosList() {
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 5;
  
    const totalPages = Math.ceil(mockUsuarios.length / itemsPerPage);
  
    const startIndex = (currentPage - 1) * itemsPerPage;
    const currentItems = mockUsuarios.slice(startIndex, startIndex + itemsPerPage);
  
    return (
      <div>
      <div className="rounded-card bg-white shadow-md border border-stroke-primary overflow-hidden">
        <div className="bg-bah-purple px-6 py-6">
          <div className="flex justify-between items-end">
            <h1 className="text-title3-semibold font-mulish text-white">
              Usuários Cadastrados
            </h1>
            <p className="text-body-regular font-mulish text-white">
              {mockUsuarios.length} usuários encontrados
            </p>
          </div>
        </div>
  
        <div className="flex px-6 py-2 bg-background-secondary">
          <h1 className="text-body-regular font-mulish">Usuário</h1>
          <h1 className="text-body-regular font-mulish ml-auto px-38">Ações</h1>
        </div>
   
        <div className="py-4 space-y-2">
          {currentItems.map((item) => (
            <UsuarioListItem
              key={item.id}
              title={item.title}
              email={item.description}
              imageUrl={item.imageUrl}
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
                  onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                />
              </PaginationItem>
  
              {Array.from({ length: totalPages }).map((_, i) => (
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
                  onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        </div>
      </div>
    );
  }
  
  export default UsuariosList;
  