export interface IniciativasListProps{
    searchQuery: string;
}
  
export interface Iniciativa{
    id: string;
    titulo: string;
    descricao: string;
    imagem_url: string;
    horarios: Horario[];
}
  
export interface IniciativasResponse{
    items: Iniciativa[];
    total: number;
}

export interface Horario {
    hora_inicio: string;
    hora_fim: string;
}

export interface SearchParams {
    q?: string;
    page?: number;
    size?: number;
}