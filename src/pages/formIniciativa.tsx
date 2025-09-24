import React, { useState, useEffect } from 'react'
import type { ChangeEvent, FormEvent, KeyboardEvent } from 'react'
import { LayoutGrid, Users, LogOut } from 'lucide-react'

interface FormData {
  titulo: string
  local: string
  link1: string
  link2: string
  organizador: string
  descricao: string
}

const iniciativaParaEditar = {
  id: 123,
  titulo: 'Iniciativa de Exemplo',
  local: 'Online',
  link1: 'https://siteprincipal.com',
  link2: 'https://sitelinkedin.com',
  organizador: 'Equipe BAH',
  descricao: 'Descrição.',
  isAtivo: false,
  tags: ['Tag1', 'Tag2'],
}

function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-screen w-48 bg-[#5a2d86] text-white p-4 rounded-r-2xl z-20">
      <a href="/" className="flex items-center">
        <div className="w-28">
          <img
            src="../src/assets/logo.png"
            alt="Logo BAH"
            className="w-full h-auto"
          />
        </div>
      </a>
      <div className="mt-8 flex flex-col">
        <span className="px-3 py-2 text-sm text-white/70 font-bold">MENU</span>
        <nav className="mt-2 flex flex-col gap-1">
          <a
            href="/iniciativas"
            className="pl-3 pr-3 py-2 rounded hover:bg-white/10 flex items-center gap-3"
          >
            <LayoutGrid size={20} />
            Iniciativas
          </a>
          <a
            href="/usuarios"
            className="pl-3 pr-3 py-2 rounded hover:bg-white/10 flex items-center gap-3"
          >
            <Users size={20} />
            Usuários
          </a>
        </nav>
      </div>
      <div className="absolute bottom-0 left-0 w-full p-4 flex justify-between items-center">
        <div className="text-sm">
          <div className="font-semibold">Admin</div>
          <div className="text-xs opacity-80">admin@exemplo.com</div>
        </div>
        <button
          onClick={() => {
            console.log('Logout clicado!')
            alert('Logout!')
          }}
          className="p-2 rounded-md hover:bg-red-500/20 text-white/80 hover:text-red-400 transition-colors"
          title="Sair"
          aria-label="Logout"
        >
          <LogOut size={20} />
        </button>
      </div>
    </aside>
  )
}

interface InitiativeCardProps {
  formData: FormData
  isAtivo: boolean
  tags: string[]
  newTag: string
  onFormChange: (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => void
  onToggleAtivo: () => void
  onNewTagChange: (e: ChangeEvent<HTMLInputElement>) => void
  onNewTagKeyDown: (e: KeyboardEvent<HTMLInputElement>) => void
  onRemoveTag: (tag: string) => void
}

function InitiativeCard({
  formData,
  isAtivo,
  tags,
  newTag,
  onFormChange,
  onToggleAtivo,
  onNewTagChange,
  onNewTagKeyDown,
  onRemoveTag,
}: InitiativeCardProps) {
  return (
    <section className="w-full">
      <div className="relative bg-white rounded-[1.5rem] p-6 border border-gray-200 shadow-sm w-full">
        <div className="absolute top-6 right-6 flex items-center gap-4">
          <button
            type="button"
            onClick={onToggleAtivo}
            aria-label={
              isAtivo ? 'Desmarcar como favorito' : 'Marcar como favorito'
            }
            className="p-1 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-800"
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="currentColor"
              className={isAtivo ? 'text-black' : 'text-gray-400'}
            >
              <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.62L12 2 9.19 8.62 2 9.24l5.46 4.73L5.82 21z" />
            </svg>
          </button>
          <label
            htmlFor="toggle-ativo"
            className="relative inline-flex items-center cursor-pointer"
          >
            <input
              type="checkbox"
              id="toggle-ativo"
              className="sr-only peer"
              checked={isAtivo}
              onChange={onToggleAtivo}
            />
            <div className="w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
          </label>
        </div>
        <h2 className="font-mulish text-lg font-bold text-black mb-6">
          Detalhes da Iniciativa
        </h2>
        <div className="grid grid-cols-1 gap-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-bold text-black mb-2">
                Título
              </label>
              <input
                type="text"
                name="titulo"
                value={formData.titulo}
                onChange={onFormChange}
                placeholder="Placeholder"
                className="w-full px-4 py-2 border-2 border-gray-300 rounded-[0.8rem] text-sm placeholder-gray-400 focus:outline-none ]"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-black mb-2">
                Local
              </label>
              <input
                type="text"
                name="local"
                value={formData.local}
                onChange={onFormChange}
                placeholder="Placeholder"
                className="w-full px-4 py-2 border-2 border-gray-300 rounded-[0.8rem] text-sm placeholder-gray-400 "
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-black mb-2">
                Link
              </label>
              <input
                type="text"
                name="link1"
                value={formData.link1}
                onChange={onFormChange}
                placeholder="Placeholder"
                className="w-full px-4 py-2 border-2 border-gray-300 rounded-[0.8rem] text-sm placeholder-gray-400 focus:outline-none focus:ring-2 "
              />
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-2">
              <label className="block text-xs font-bold text-black mb-2">
                Link
              </label>
              <input
                type="text"
                name="link2"
                value={formData.link2}
                onChange={onFormChange}
                placeholder="Placeholder"
                className="w-full px-4 py-2 border-2 border-gray-300 rounded-[0.8rem] text-sm placeholder-gray-400 focus:outline-none focus:ring-2"
              />
            </div>
            <div className="md:col-span-1">
              <label className="block text-xs font-bold text-black mb-2">
                Organizador
              </label>
              <select
                name="organizador"
                value={formData.organizador}
                onChange={onFormChange}
                className="w-full px-4 py-2 border-2 border-gray-300 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-2"
              >
                <option value="">Placeholder</option>
                <option value="Equipe BAH">Equipe BAH</option>
              </select>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-2">
              <label className="block text-xs font-bold text-black mb-2">
                Descrição
              </label>
              <textarea
                name="descricao"
                value={formData.descricao}
                onChange={onFormChange}
                placeholder="Entry Requirements"
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-[0.8rem] text-sm placeholder-gray-400 h-28 resize-y focus:outline-none focus:ring-2"
              />
            </div>
            <div className="md:col-span-1">
              <label className="block text-xs font-bold text-black mb-2">
                Tags
              </label>
              <div className="w-full border-2 border-gray-300 rounded-[1rem] min-h-[7rem] p-3 flex flex-col">
                <div className="flex flex-wrap gap-2">
                  {tags.map(tag => (
                    <span
                      key={tag}
                      className="inline-flex items-center gap-1 bg-lime-200 text-lime-800 text-sm font-medium pl-3 pr-2 py-1 rounded-full"
                    >
                      {tag}
                      <button
                        type="button"
                        onClick={() => onRemoveTag(tag)}
                        className="text-lime-700 hover:text-lime-900"
                        aria-label={`Remover tag ${tag}`}
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="14"
                          height="14"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2.5"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        >
                          <circle cx="12" cy="12" r="10"></circle>
                          <line x1="15" y1="9" x2="9" y2="15"></line>
                          <line x1="9" y1="9" x2="15" y2="15"></line>
                        </svg>
                      </button>
                    </span>
                  ))}
                </div>
                <input
                  type="text"
                  value={newTag}
                  onChange={onNewTagChange}
                  onKeyDown={onNewTagKeyDown}
                  placeholder="Adicionar tag..."
                  className="w-full mt-auto pt-2 border-t border-gray-200 text-sm placeholder-gray-400 focus:outline-none bg-transparent"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default function FormIniciativa() {
  const [isEditing, setIsEditing] = useState(false)
  const [formData, setFormData] = useState<FormData>({
    titulo: '',
    local: '',
    link1: '',
    link2: '',
    organizador: '',
    descricao: '',
  })
  const [isAtivo, setIsAtivo] = useState(true)
  const [tags, setTags] = useState<string[]>([])
  const [newTag, setNewTag] = useState('')

  interface Schedule {
    id: string
    dia: string
    inicio: string
    fim: string
    tipo: string
  }
  const [schedules, setSchedules] = useState<Schedule[]>([])

  const makeId = () => String(Date.now()) + Math.floor(Math.random() * 1000)

  const handleAddSchedule = () => {
    setSchedules(prev => [
      ...prev,
      { id: makeId(), dia: '', inicio: '', fim: '', tipo: '' },
    ])
  }

  const handleRemoveSchedule = (id: string) => {
    setSchedules(prev => prev.filter(s => s.id !== id))
  }

  const handleScheduleChange = (
    id: string,
    field: keyof Omit<Schedule, 'id'>,
    value: string
  ) => {
    setSchedules(prev =>
      prev.map(s => (s.id === id ? { ...s, [field]: value } : s))
    )
  }

  useEffect(() => {
    if (isEditing) {
      setFormData({
        titulo: iniciativaParaEditar.titulo,
        local: iniciativaParaEditar.local,
        link1: iniciativaParaEditar.link1,
        link2: iniciativaParaEditar.link2,
        organizador: iniciativaParaEditar.organizador,
        descricao: iniciativaParaEditar.descricao,
      })
      setIsAtivo(iniciativaParaEditar.isAtivo)
      setTags(iniciativaParaEditar.tags)
      // exemplo: popular schedules se viesse do backend
      setSchedules([
        {
          id: makeId(),
          dia: 'segunda',
          inicio: '09:00',
          fim: '11:00',
          tipo: 'online',
        },
      ])
    } else {
      setFormData({
        titulo: '',
        local: '',
        link1: '',
        link2: '',
        organizador: '',
        descricao: '',
      })
      setTags([])
      setSchedules([])
    }
  }, [isEditing])

  const handleFormChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleToggleAtivo = () => {
    setIsAtivo(current => !current)
  }

  const handleNewTagChange = (e: ChangeEvent<HTMLInputElement>) => {
    setNewTag(e.target.value)
  }

  const handleAddTag = () => {
    const trimmedTag = newTag.trim()
    if (trimmedTag && !tags.includes(trimmedTag)) {
      setTags(prev => [...prev, trimmedTag])
    }
    setNewTag('')
  }

  const handleNewTagKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      handleAddTag()
    }
  }

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(prev => prev.filter(tag => tag !== tagToRemove))
  }

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    const payload = { ...formData, isAtivo, tags, schedules }
    if (isEditing) {
      alert('Lógica para ATUALIZAR a iniciativa. Veja o console.')
      console.log('Atualizando com:', payload)
    } else {
      alert('Lógica para CRIAR uma nova iniciativa. Veja o console.')
      console.log('Criando com:', payload)
    }
  }

  return (
    <>
      <Sidebar />
      <main className="ml-64 p-6 min-h-screen bg-gray-50">
        <header className="mb-6 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-mulish text-[#5a2d86]">
              {isEditing ? 'Editar Iniciativa' : 'Criar Iniciativa'}
            </h1>
            <p className="text-sm text-gray-600">
              {isEditing ? `Editar a iniciativa` : 'Criar iniciativa'}
            </p>
          </div>
          <button
            onClick={() => setIsEditing(!isEditing)}
            className="text-sm bg-gray-200 px-4 py-2 rounded-lg hover:bg-gray-300"
          >
            {isEditing ? 'Cancelar Edição' : 'Editar'}
          </button>
        </header>

        <form onSubmit={handleSubmit}>
          <div className="w-full">
            <InitiativeCard
              formData={formData}
              isAtivo={isAtivo}
              tags={tags}
              newTag={newTag}
              onFormChange={handleFormChange}
              onToggleAtivo={handleToggleAtivo}
              onNewTagChange={handleNewTagChange}
              onNewTagKeyDown={handleNewTagKeyDown}
              onRemoveTag={handleRemoveTag}
            />
          </div>

          <section className="w-full mt-8">
            <div className="bg-white rounded-[1.5rem] p-6 border border-gray-200 shadow-sm w-full">
              <div className="flex justify-between items-center mb-6">
                <h2 className="font-mulish text-lg font-bold text-black">
                  Horários
                </h2>

                <div className="flex flex-col items-center">
                  <span className="text-sm text-black font-bold mb-2">
                    Clique para adicionar
                  </span>

                  <button
                    type="button"
                    onClick={handleAddSchedule}
                    className="px-4 py-2 w-30 h-10 rounded-[0.8rem] bg-[#f2f2f7] text-[#85858b] text-sm hover:opacity-90"
                    aria-label="Adicionar horário"
                  >
                    +
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {schedules.length === 0 && (
                  <div className="col-span-full text-sm text-gray-500">
                    Nenhum horário adicionado — clique em + para adicionar.
                  </div>
                )}

                {schedules.map(schedule => (
                  <div
                    key={schedule.id}
                    className="bg-gray-50 rounded-[1rem] p-4 border border-gray-100 flex flex-col gap-3"
                  >
                    <div className="flex justify-between items-start">
                      <div className="text-sm font-semibold">Horário</div>
                      <button
                        type="button"
                        onClick={() => handleRemoveSchedule(schedule.id)}
                        className="text-red-500 text-sm px-2 py-1 rounded hover:bg-red-50"
                        aria-label="Remover horário"
                      >
                        Remover
                      </button>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs font-bold text-black mb-2">
                          Dia
                        </label>
                        <select
                          value={schedule.dia}
                          onChange={e =>
                            handleScheduleChange(
                              schedule.id,
                              'dia',
                              e.target.value
                            )
                          }
                          className={`w-full px-4 py-2 border border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#5a2d86] ${
                            schedule.dia === '' ? 'text-gray-400' : 'text-black'
                          }`}
                        >
                          <option value="" disabled hidden>
                            Selecione o dia
                          </option>
                          <option value="segunda">Segunda-feira</option>
                          <option value="terca">Terça-feira</option>
                          <option value="quarta">Quarta-feira</option>
                          <option value="quinta">Quinta-feira</option>
                          <option value="sexta">Sexta-feira</option>
                          <option value="sabado">Sábado</option>
                          <option value="domingo">Domingo</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-xs font-bold text-black mb-2">
                          Tipo
                        </label>
                        <select
                          value={schedule.tipo}
                          onChange={e =>
                            handleScheduleChange(
                              schedule.id,
                              'tipo',
                              e.target.value
                            )
                          }
                          className={`w-full px-4 py-2 border border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#5a2d86] ${
                            schedule.tipo === ''
                              ? 'text-gray-400'
                              : 'text-black'
                          }`}
                        >
                          <option value="" disabled hidden>
                            Selecione o tipo
                          </option>
                          <option value="presencial">Presencial</option>
                          <option value="online">Online</option>
                          <option value="hibrido">Híbrido</option>
                        </select>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs font-bold text-black mb-2">
                          Horário Início
                        </label>
                        <select
                          value={schedule.inicio}
                          onChange={e =>
                            handleScheduleChange(
                              schedule.id,
                              'inicio',
                              e.target.value
                            )
                          }
                          className={`w-full px-4 py-2 border border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#5a2d86] ${
                            schedule.inicio === ''
                              ? 'text-gray-400'
                              : 'text-black'
                          }`}
                        >
                          <option value="" disabled hidden>
                            Selecione o horário
                          </option>
                          <option value="08:00">08:00</option>
                          <option value="09:00">09:00</option>
                          <option value="10:00">10:00</option>
                          <option value="11:00">11:00</option>
                          <option value="12:00">12:00</option>
                          <option value="13:00">13:00</option>
                          <option value="14:00">14:00</option>
                          <option value="15:00">15:00</option>
                          <option value="16:00">16:00</option>
                          <option value="17:00">17:00</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-xs font-bold text-black mb-2">
                          Horário Fim
                        </label>
                        <select
                          value={schedule.fim}
                          onChange={e =>
                            handleScheduleChange(
                              schedule.id,
                              'fim',
                              e.target.value
                            )
                          }
                          className={`w-full px-4 py-2 border border-gray-200 rounded-[0.8rem] text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#5a2d86] ${
                            schedule.fim === '' ? 'text-gray-400' : 'text-black'
                          }`}
                        >
                          <option value="" disabled hidden>
                            Selecione o horário
                          </option>
                          <option value="09:00">09:00</option>
                          <option value="10:00">10:00</option>
                          <option value="11:00">11:00</option>
                          <option value="12:00">12:00</option>
                          <option value="13:00">13:00</option>
                          <option value="14:00">14:00</option>
                          <option value="15:00">15:00</option>
                          <option value="16:00">16:00</option>
                          <option value="17:00">17:00</option>
                          <option value="18:00">18:00</option>
                        </select>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section className="w-full mt-8">
            <div className="bg-white rounded-[1.5rem] p-6 border border-gray-200 shadow-sm w-full">
              <h2 className="font-mulish text-lg font-bold text-black mb-6">
                Foto
              </h2>
              <label className="flex items-center justify-center w-full h-64 bg-gray-100 border border-gray-300 rounded-[1.5rem] cursor-pointer hover:bg-gray-200 transition">
                <div className="text-center text-gray-500 text-sm flex items-center gap-2">
                  <img
                    src="../src/assets/camera.png"
                    alt="Logo"
                    className="w-5 h-5"
                  />
                  <span>Clique para adicionar uma foto</span>
                  <input type="file" className="hidden" />
                </div>
              </label>
            </div>
          </section>

          <div className="mt-6 flex justify">
            <button
              type="submit"
              className="px-7 py-2 rounded-lg bg-[#5a2d86] font-mulish text-white text-sm hover:opacity-90 mt-5"
            >
              {isEditing ? 'Atualizar Iniciativa' : 'Salvar Iniciativa'}
            </button>
          </div>
        </form>
      </main>
    </>
  )
}
