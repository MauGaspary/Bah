import base64
import hashlib
import re


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def hash_url_to_base64(url: str) -> str:
    """
    Gera uma representação base64 de um hash SHA-256 para a URL informada.
    Retorna string url-safe (sem padding).
    """
    if not url:
        raise ValueError("URL não pode ser vazia para hashing")

    digest = hashlib.sha256(url.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")
