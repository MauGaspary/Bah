export interface IniciativasListProps{
    searchQuery: string;
}
  
export interface Iniciativa{
    id: number;
    titulo: string;
    descricao: string;
    imagem_url: string;
}
  
export interface IniciativasResponse{
    items: Iniciativa[];
    total: number;
}