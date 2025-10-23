import api from './api'
import type { Iniciativa, IniciativasResponse, SearchParams } from '@/interfaces/IIniciativas'

export async function searchIniciativas(params: SearchParams = {}): Promise<IniciativasResponse> {
    const response = await api.get<IniciativasResponse>('/iniciativas/search', {
        params: {
            q: params.q || '',
            page: params.page || 1,
            size: params.size || 10,
        },
    })
    return response.data
}

export async function getIniciativaById(id: string): Promise<Iniciativa> {
    const response = await api.get<Iniciativa>(`/iniciativas/${id}`)
    return response.data
}