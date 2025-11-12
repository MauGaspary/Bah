import api from './api'
import type { CalendarioMensalResponse } from '@/interfaces/ICalendario'

export async function fetchCalendarioMensal(dateISO: string): Promise<CalendarioMensalResponse> {
  const response = await api.get<CalendarioMensalResponse>('/iniciativas/calendario', {
    params: { data: dateISO },
  })
  return response.data
}


