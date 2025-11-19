export type CalendarioHorarioTipo = 'PRESENCIAL' | 'ONLINE' | 'HIBRIDO'

export interface CalendarioTag {
  id: string
  nome: string
}

export interface CalendarioIniciativaItem {
  iniciativa_id: string
  horario_id: string
  titulo: string
  descricao: string
  hora_inicio: string
  hora_fim: string
  tipo: CalendarioHorarioTipo
  link: string
  local?: string
  destaque: boolean
  tags: CalendarioTag[]
  imagem_url?: string
}

export interface DiaCalendario {
  data: string // ISO date (YYYY-MM-DD)
  iniciativas: CalendarioIniciativaItem[]
}

export interface CalendarioMensalResponse {
  mes: string // e.g. "2025-11"
  dias: DiaCalendario[]
}


