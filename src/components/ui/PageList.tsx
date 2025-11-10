import React from "react";

type Props = {
  totalPages: number;
  page: number;
  setPage: (p: number) => void;
  wrapperClassName?: string;
};

export const SimplePagination: React.FC<Props> = ({
  totalPages,
  page,
  setPage,
  wrapperClassName = "py-4 fixed bottom-0 right-0 left-[15%]"
}) => {
  if (totalPages <= 1) return null;

  return (
    <div className={wrapperClassName}>
      <div className="py-8 flex justify-center">
        <nav className="inline-flex items-center space-x-2" aria-label="Pagination">
          <button
            onClick={() => setPage(Math.max(1, page - 1))}
            disabled={page === 1}
            className="px-3 py-1 rounded disabled:opacity-50"
          >
            ←
          </button>

          {[...Array(totalPages).keys()].map(i => {
            const p = i + 1;
            return (
              <button
                key={p}
                onClick={() => setPage(p)}
                aria-current={p === page ? "page" : undefined}
                className={`min-w-[36px] h-8 px-2 rounded text-sm ${
                  p === page ? "bg-bah-purple text-white" : "hover:bg-bah-purple/20 bg-bah-purple/10"
                }`}
              >
                {p}
              </button>
            );
          })}

          <button
            onClick={() => setPage(Math.min(totalPages, page + 1))}
            disabled={page === totalPages}
            className="px-3 py-1 rounded disabled:opacity-50"
          >
            →
          </button>
        </nav>
      </div>
    </div>
  );
};

export default SimplePagination;