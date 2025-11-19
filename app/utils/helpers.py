import base64
import hashlib
import re

import httpx


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def process_image_input(image_input: str) -> str:
    """
    Processa entrada de imagem e SEMPRE retorna base64 puro:
    1. Data URI (data:image/png;base64,...) -> extrai base64
    2. URL (http://.../https://...) -> baixa e converte para base64
    3. Base64 puro -> valida e retorna
    
    Retorna: String base64 limpa (sem prefixo data:image)
    """
    if not image_input:
        raise ValueError("Imagem não pode ser vazia")
    
    image_input = image_input.strip()
    
    if image_input.startswith("data:image/"):
        if ";base64," in image_input:
            return image_input.split(";base64,", 1)[1]
        raise ValueError("Data URI inválida - formato esperado: data:image/...;base64,...")
    
    if image_input.startswith(("http://", "https://")):
        try:
            response = httpx.get(image_input, timeout=10.0)
            response.raise_for_status()
            image_bytes = response.content
            return base64.b64encode(image_bytes).decode('utf-8')
        except httpx.HTTPError as e:
            raise ValueError(f"Erro ao baixar imagem da URL: {str(e)}") from e
    
    try:
        base64.b64decode(image_input, validate=True)
        return image_input
    except Exception as e:
        raise ValueError("Formato inválido: não é URL, data URI ou base64 válido") from e


def hash_url_to_base64(url: str) -> str:
    """
    DEPRECATED: Use process_image_input() para novos códigos.
    
    Gera uma representação base64 de um hash SHA-256 para a URL informada.
    Retorna string url-safe (sem padding).
    """
    if not url:
        raise ValueError("URL não pode ser vazia para hashing")

    digest = hashlib.sha256(url.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")
