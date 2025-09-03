export interface NavigationItem {
  id: string
  label: string
  path: string
}

export const optionsItems: NavigationItem[] = [
  {
    id: 'calendario',
    label: 'Calendário',
    path: '/calendario',
  },
  {
    id: 'jornada',
    label: 'Jornada',
    path: '/jornada',
  },
  {
    id: 'sobre nos',
    label: 'Sobre nós',
    path: '/sobre-nos',
  },
  {
    id: 'nossos-valores',
    label: 'Nossos Valores',
    path: '/nossos-valores',
  },
  {
    id: 'contato',
    label: 'Contato',
    path: '/contato',
  },
]
