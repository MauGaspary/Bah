export enum HorarioTipo {
  PRESENCIAL = 'presencial',
  HIBRIDO = 'hibrido',
  ONLINE = 'online',
}

export const HORARIO_TIPO_LABELS = {
  [HorarioTipo.PRESENCIAL]: 'Presencial',
  [HorarioTipo.HIBRIDO]: 'Híbrido',
  [HorarioTipo.ONLINE]: 'Online',
} as const
