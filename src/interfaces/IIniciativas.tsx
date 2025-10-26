import { HorarioTipo } from '@/enums/HorarioTipo'

export interface IniciativasListProps {
  searchQuery: string
}

export interface IniciativaHorarioCreate {
  data_evento: string // ISO date string (YYYY-MM-DD)
  hora_inicio: string // ISO time string (HH:MM:SS)
  hora_fim: string // ISO time string (HH:MM:SS)
  tipo: HorarioTipo
}

export interface IniciativaHorarioResponse {
  id: string
  data_evento: string // ISO date string (YYYY-MM-DD)
  hora_inicio: string // ISO time string (HH:MM:SS)
  hora_fim: string // ISO time string (HH:MM:SS)
  tipo: HorarioTipo
  criado_em?: string // ISO datetime string
}

export interface IniciativaCreate {
  titulo: string
  descricao: string
  organizador_id: string
  link: string
  local?: string
  imagem_url: string
  destaque: boolean
  horarios: IniciativaHorarioCreate[]
  tag_ids?: string[]
  descricoes_extras?: string[]
}

export interface IniciativaResponse {
  id: string
  titulo: string
  descricao: string
  organizador_id?: string
  link: string
  local?: string
  imagem_url: string
  destaque: boolean
  horarios: IniciativaHorarioResponse[]
  criado_em?: string // ISO datetime string
  criado_por?: string
  editado_em?: string // ISO datetime string
  editado_por?: string
}

export interface IniciativaFilters {
  q?: string
  page: number
  size: number
}

export interface IniciativasResponse {
  items: IniciativaResponse[]
  total: number
  filters: IniciativaFilters
}

// Type aliases para compatibilidade com código existente
export type Iniciativa = IniciativaResponse
export type IniciativaHorario = IniciativaHorarioResponse
