import React from 'react'

export interface ContactFormState {
  nomeCompleto: string
  email: string
  assunto: string
  mensagem: string
}

export interface ContactInfoItemProps {
  icon: React.ReactNode
  title: string
  content: string
}

export interface SocialMediaLinkProps {
  icon: React.ReactNode
  href: string
  color: string
}
