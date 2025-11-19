/**
 * Constrói a URL completa para uma imagem
 * @param imagePath - Caminho relativo ou URL completa da imagem
 * @returns URL completa da imagem
 */
export function getImageUrl(imagePath: string | undefined): string | undefined {
  if (!imagePath) return undefined

  // Se já é uma URL completa, retornar como está
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath
  }

  // Se é caminho relativo, construir URL com base da API
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  return `${API_BASE_URL}/uploads${imagePath}`
}



