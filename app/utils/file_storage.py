"""Utilitário para gerenciar upload e armazenamento de arquivos."""

import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import UploadFile


class FileStorage:
    """Gerencia upload e armazenamento de arquivos."""

    def __init__(self, base_path: str = "uploads"):
        """
        Inicializa o gerenciador de arquivos.

        Args:
            base_path: Caminho base para armazenamento de arquivos
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_image(self, file: UploadFile, subfolder: str = "iniciativas") -> str:
        """
        Salva uma imagem no sistema de arquivos.

        Args:
            file: Arquivo de upload do FastAPI
            subfolder: Subpasta para organizar arquivos

        Returns:
            Caminho relativo do arquivo salvo

        Raises:
            ValueError: Se o arquivo não for uma imagem válida
        """
        # Validar tipo de arquivo
        if not file.content_type or not file.content_type.startswith("image/"):
            raise ValueError(
                f"Tipo de arquivo inválido: {file.content_type}. Apenas imagens são permitidas."
            )

        # Validar extensão
        allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        file_ext = Path(file.filename or "").suffix.lower()
        if file_ext not in allowed_extensions:
            raise ValueError(
                f"Extensão de arquivo inválida: {file_ext}. Extensões permitidas: {', '.join(allowed_extensions)}"
            )

        # Criar subpasta se não existir
        upload_dir = self.base_path / subfolder
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Gerar nome único para o arquivo
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = upload_dir / unique_filename

        # Salvar arquivo
        try:
            with open(file_path, "wb") as buffer:
                content = file.file.read()
                buffer.write(content)
        except Exception as e:
            raise RuntimeError(f"Erro ao salvar arquivo: {str(e)}") from e
        finally:
            file.file.close()

        # Retornar caminho relativo
        return f"/{subfolder}/{unique_filename}"

    def delete_image(self, relative_path: str) -> bool:
        """
        Remove uma imagem do sistema de arquivos.

        Args:
            relative_path: Caminho relativo da imagem (ex: /iniciativas/uuid.jpg)

        Returns:
            True se o arquivo foi removido, False se não existia
        """
        # Remover barra inicial se existir
        relative_path = relative_path.lstrip("/")

        file_path = self.base_path / relative_path

        if file_path.exists() and file_path.is_file():
            try:
                file_path.unlink()
                return True
            except Exception as e:
                print(f"Erro ao deletar arquivo {file_path}: {str(e)}")
                return False

        return False

    def get_absolute_path(self, relative_path: str) -> Optional[Path]:
        """
        Converte caminho relativo em caminho absoluto.

        Args:
            relative_path: Caminho relativo da imagem

        Returns:
            Path absoluto do arquivo ou None se não existir
        """
        relative_path = relative_path.lstrip("/")
        file_path = self.base_path / relative_path

        if file_path.exists() and file_path.is_file():
            return file_path

        return None


# Instância singleton para uso na aplicação
file_storage = FileStorage(base_path=os.getenv("UPLOAD_PATH", "uploads"))




