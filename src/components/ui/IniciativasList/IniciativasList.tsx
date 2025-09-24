
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";

import { useState } from "react";
import ListItem from "./ListItem";

const mockIniciativas = Array.from({ length: 22 }).map((_, i) => ({
  id: i + 1,
  title: `Iniciativa ${i + 1  }`,
  description: "Descrição da iniciativa",
  imageUrl: "https://placehold.co/150x150.png?text=",
  
}));

function IniciativasList() {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  const totalPages = Math.ceil(mockIniciativas.length / itemsPerPage);

  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentItems = mockIniciativas.slice(startIndex, startIndex + itemsPerPage);

  return (
    <div>
    <div className="rounded-card bg-white shadow-md overflow-hidden">
      <div className="bg-bah-purple px-6 py-6">
        <div className="flex justify-between items-end mt-3">
          <h1 className="text-medium-title font-mulish text-white">
            Iniciativas Cadastradas
          </h1>
          <p className="text-body-regular font-mulish text-white">
            {mockIniciativas.length} iniciativas encontradas
          </p>
        </div>
      </div>

      <div className="flex px-6 py-2 bg-background-secondary justify-between">
        <h1 className="text-body-regular font-mulish">Iniciativa</h1>
        <h1 className="text-body-regular font-mulish mr-53.5">Ações</h1>
      </div>
 
      <div className="py-3 space-y-2 ">
        {currentItems.map((item, index) => (
          <ListItem
            key={item.id}
            title={item.title}
            description={item.description}
            imageUrl={item.imageUrl}
            isLast={index === currentItems.length - 1}
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

export default IniciativasList;
