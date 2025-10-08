// Tipos baseados nos esquemas fornecidos pelo usuário e no CalendarEvent do componente
import type { CalendarEvent } from '@/components/ui/CalendarSection/CalendarSection'

export type Iniciativa = {
  id: string
  titulo: string
  descricao: string
  descricao_vetor: number[] // placeholder local; no backend seria vector[]
  organizador_id: string
  link: string
  destaque: boolean
  local?: string
  imagem_url: string
  criado_por: string
  criado_em?: string
  editado_em?: string
  editado_por?: string
  deletado_em?: string
  deletado_por?: string
}

export type EventoDeIniciativa = {
  id: string
  iniciativa_id: string
  data_evento: string // yyyy-mm-dd
  hora_inicio: string // HH:mm
  hora_fim: string // HH:mm
  criado_em?: string
  tipo: 'networking' | 'feira' | 'meetup' | 'workshop' | 'hackathon'
}

function isoDate(d: Date) {
  return d.toISOString().slice(0, 10)
}

function addDays(base: Date, days: number) {
  const d = new Date(base)
  d.setDate(d.getDate() + days)
  return d
}

// Datas relativas: entre mês passado e 2 meses à frente
const today = new Date()
const start = addDays(today, -30)

export const iniciativas: Iniciativa[] = [
  {
    id: '11111111-1111-1111-1111-111111111111',
    titulo: 'Feira de Startups Caxias',
    descricao: 'Exposição de startups locais e pitches para investidores.',
    descricao_vetor: [0.1, 0.2, 0.3],
    organizador_id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    link: 'https://exemplo.com/feira-startups',
    destaque: true,
    local: 'Caxias do Sul - Parque de Eventos',
    imagem_url: 'https://images.unsplash.com/photo-1552664730-d307ca884978?q=80&w=1600&auto=format&fit=crop',
    criado_por: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
  },
  {
    id: '22222222-2222-2222-2222-222222222222',
    titulo: 'Meetup de Devs Serra Gaúcha',
    descricao: 'Encontro mensal de desenvolvedores para talks e networking.',
    descricao_vetor: [0.2, 0.1, 0.5],
    organizador_id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    link: 'https://exemplo.com/meetup-devs',
    destaque: true,
    local: 'TecnoUCS',
    imagem_url: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=1600&auto=format&fit=crop',
    criado_por: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
  },
  {
    id: '33333333-3333-3333-3333-333333333333',
    titulo: 'Workshop de UX Research',
    descricao: 'Oficina prática de técnicas de pesquisa com usuários.',
    descricao_vetor: [0.4, 0.1, 0.2],
    organizador_id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    link: 'https://exemplo.com/workshop-ux',
    destaque: false,
    local: 'Online',
    imagem_url: 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?q=80&w=1600&auto=format&fit=crop',
    criado_por: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
  },
  {
    id: '44444444-4444-4444-4444-444444444444',
    titulo: 'Hackathon Indústria 4.0',
    descricao: 'Maratona de 24h focada em desafios da indústria.',
    descricao_vetor: [0.3, 0.6, 0.2],
    organizador_id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    link: 'https://exemplo.com/hackathon-i40',
    destaque: true,
    local: 'Senai Caxias',
    imagem_url: 'https://images.unsplash.com/photo-1553877522-43269d4ea984?q=80&w=1600&auto=format&fit=crop',
    criado_por: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
  },
  {
    id: '55555555-5555-5555-5555-555555555555',
    titulo: 'Networking Mulheres na Tecnologia',
    descricao: 'Roda de conversa e conexões para mulheres na TI.',
    descricao_vetor: [0.7, 0.1, 0.1],
    organizador_id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    link: 'https://exemplo.com/networking-mulheres',
    destaque: false,
    local: 'Coworking Downtown',
    imagem_url: 'https://images.unsplash.com/photo-1559136555-9303baea8ebd?q=80&w=1600&auto=format&fit=crop',
    criado_por: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
  },
  {
    id: '66666666-6666-6666-6666-666666666666',
    titulo: 'Feira Universitária de Inovação',
    descricao: 'Projetos acadêmicos com foco em inovação aplicada.',
    descricao_vetor: [0.2, 0.8, 0.2],
    organizador_id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    link: 'https://exemplo.com/feira-universitaria',
    destaque: true,
    local: 'UCS',
    imagem_url: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?q=80&w=1600&auto=format&fit=crop',
    criado_por: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
  },
  {
    id: '77777777-7777-7777-7777-777777777777',
    titulo: 'Meetup IA Generativa',
    descricao: 'Casos práticos de IA generativa em negócios.',
    descricao_vetor: [0.3, 0.3, 0.3],
    organizador_id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    link: 'https://exemplo.com/meetup-ia',
    destaque: false,
    local: 'Online',
    imagem_url: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=1600&auto=format&fit=crop',
    criado_por: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
  },
  {
    id: '88888888-8888-8888-8888-888888888888',
    titulo: 'Workshop de Segurança em APIs',
    descricao: 'Boas práticas de segurança para APIs modernas.',
    descricao_vetor: [0.5, 0.4, 0.1],
    organizador_id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    link: 'https://exemplo.com/workshop-seguranca',
    destaque: false,
    local: 'TecnoUCS',
    imagem_url: 'https://images.unsplash.com/photo-1518773553398-650c184e0bb3?q=80&w=1600&auto=format&fit=crop',
    criado_por: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
  },
  {
    id: '99999999-9999-9999-9999-999999999999',
    titulo: 'Feira de Empreendedorismo Jovem',
    descricao: 'Exposição e mentorias para jovens empreendedores.',
    descricao_vetor: [0.6, 0.2, 0.2],
    organizador_id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    link: 'https://exemplo.com/feira-jovem',
    destaque: true,
    local: 'Centro de Eventos Municipal',
    imagem_url: 'https://images.unsplash.com/photo-1543269865-cbf427effbad?q=80&w=1600&auto=format&fit=crop',
    criado_por: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
  },
  {
    id: 'aaaaaaaa-0000-0000-0000-000000000000',
    titulo: 'Hackathon Sustentabilidade',
    descricao: 'Soluções verdes para cidades inteligentes.',
    descricao_vetor: [0.2, 0.2, 0.7],
    organizador_id: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    link: 'https://exemplo.com/hackathon-sustentavel',
    destaque: false,
    local: 'Online',
    imagem_url: 'https://images.unsplash.com/photo-1556761175-129418cb2dfe?q=80&w=1600&auto=format&fit=crop',
    criado_por: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
  },
]

export const eventos: EventoDeIniciativa[] = [
  // Datas distribuídas: -30 a +60 dias
  {
    id: 'e1',
    iniciativa_id: '11111111-1111-1111-1111-111111111111',
    data_evento: isoDate(addDays(start, 2)),
    hora_inicio: '09:00',
    hora_fim: '18:00',
    tipo: 'feira',
  },
  {
    id: 'e2',
    iniciativa_id: '22222222-2222-2222-2222-222222222222',
    data_evento: isoDate(addDays(start, 6)),
    hora_inicio: '19:00',
    hora_fim: '21:00',
    tipo: 'meetup',
  },
  {
    id: 'e3',
    iniciativa_id: '33333333-3333-3333-3333-333333333333',
    data_evento: isoDate(addDays(start, 12)),
    hora_inicio: '14:00',
    hora_fim: '17:00',
    tipo: 'workshop',
  },
  {
    id: 'e4',
    iniciativa_id: '44444444-4444-4444-4444-444444444444',
    data_evento: isoDate(addDays(start, 18)),
    hora_inicio: '10:00',
    hora_fim: '10:00',
    tipo: 'hackathon',
  },
  {
    id: 'e5',
    iniciativa_id: '55555555-5555-5555-5555-555555555555',
    data_evento: isoDate(addDays(start, 37)),
    hora_inicio: '18:30',
    hora_fim: '20:30',
    tipo: 'networking',
  },
  {
    id: 'e6',
    iniciativa_id: '66666666-6666-6666-6666-666666666666',
    data_evento: isoDate(addDays(start, 30)),
    hora_inicio: '08:30',
    hora_fim: '17:30',
    tipo: 'feira',
  },
  {
    id: 'e7',
    iniciativa_id: '77777777-7777-7777-7777-777777777777',
    data_evento: isoDate(addDays(start, 37)),
    hora_inicio: '19:30',
    hora_fim: '21:00',
    tipo: 'meetup',
  },
  {
    id: 'e8',
    iniciativa_id: '88888888-8888-8888-8888-888888888888',
    data_evento: isoDate(addDays(start, 45)),
    hora_inicio: '09:00',
    hora_fim: '12:00',
    tipo: 'workshop',
  },
  {
    id: 'e9',
    iniciativa_id: '99999999-9999-9999-9999-999999999999',
    data_evento: isoDate(addDays(start, 52)),
    hora_inicio: '10:00',
    hora_fim: '18:00',
    tipo: 'feira',
  },
  {
    id: 'e10',
    iniciativa_id: 'aaaaaaaa-0000-0000-0000-000000000000',
    data_evento: isoDate(addDays(start, 60)),
    hora_inicio: '09:00',
    hora_fim: '12:00',
    tipo: 'hackathon',
  },
]

export function buildCalendarEvents(): CalendarEvent[] {
  const iniciativaById = new Map(iniciativas.map(i => [i.id, i]))
  return eventos.map(ev => {
    const ini = iniciativaById.get(ev.iniciativa_id)
    const title = ini ? ini.titulo : 'Evento'
    const description = ini ? ini.descricao : undefined
    const location = ini?.local
    const imageUrl = ini?.imagem_url
    return {
      id: ev.id,
      title,
      description,
      date: ev.data_evento,
      category: ev.tipo,
      location,
      imageUrl,
      featured: ini?.destaque === true,
    } satisfies CalendarEvent
  })
}


