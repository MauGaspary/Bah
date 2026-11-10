import { HorarioTipo } from '@/enums/HorarioTipo'

export interface IniciativasListProps {
  searchQuery: string
}

export interface IniciativasResponse {
  items: Iniciativa[]
  total: number
}

export interface SearchParams {
  q?: string
  page?: number
  size?: number
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

// Type aliases para compatibilidade com código existente
export type Iniciativa = IniciativaResponse
export type IniciativaHorario = IniciativaHorarioResponse

// Admin shapes (backend returns IniciativaSchema with extras like tags and descricoes)
export interface IniciativaAdminTag {
  id: string
  nome: string
}

export interface IniciativaAdminDescricaoExtra {
  id: string
  descricao: string
}

export interface IniciativaAdmin extends IniciativaResponse {
  tags: IniciativaAdminTag[]
  descricoes_extras: IniciativaAdminDescricaoExtra[]
  organizador?: { id: string; nome: string }
}

export interface IniciativaHorarioPatch {
  data_evento?: string
  hora_inicio?: string
  hora_fim?: string
  tipo?: HorarioTipo
}

export interface IniciativaPatch {
  titulo?: string
  descricao?: string
  link?: string
  destaque?: boolean
  local?: string
  imagem_url?: string
  organizador_id?: string
  tags_ids?: string[]
  horarios?: IniciativaHorarioPatch[]
  descricoes_extras_update?: { id: string; descricao: string }[]
  descricoes_extras_delete_ids?: string[]
  descricoes_extras_add?: string[]
}
