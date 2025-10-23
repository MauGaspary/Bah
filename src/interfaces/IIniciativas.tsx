export interface IniciativasListProps{
    searchQuery: string;
}
  
export interface Iniciativa{
    id: string;
    titulo: string;
    descricao: string;
    imagem_url: string;
    link?: string;
    horarios: Horario[];
}
  
export interface IniciativasResponse{
    items: Iniciativa[];
    total: number;
}

export interface Horario {
    id?: string;
    hora_inicio: string;
    hora_fim: string;
    data: string;
    dia: string;
    modalidade: string;
}

export interface SearchParams {
    q?: string;
    page?: number;
    size?: number;
}