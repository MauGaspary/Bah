"""Testes para funcionalidade de upload de arquivos."""

import io
import json
from datetime import date, time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.utils.file_storage import FileStorage, file_storage


class TestFileStorage:
    """Testes para o FileStorage."""

    def test_save_image_valid_jpg(self, tmp_path):
        """Testa salvamento de imagem JPG válida."""
        storage = FileStorage(base_path=str(tmp_path))

        # Criar arquivo fake
        fake_image = io.BytesIO(b"fake image content")
        from fastapi import UploadFile

        upload_file = UploadFile(
            filename="test.jpg", file=fake_image, content_type="image/jpeg"
        )

        # Salvar imagem
        saved_path = storage.save_image(upload_file, subfolder="test")

        # Verificar resultado
        assert saved_path.startswith("/test/")
        assert saved_path.endswith(".jpg")

        # Verificar que arquivo existe
        full_path = tmp_path / "test" / Path(saved_path).name
        assert full_path.exists()

    def test_save_image_valid_png(self, tmp_path):
        """Testa salvamento de imagem PNG válida."""
        storage = FileStorage(base_path=str(tmp_path))

        fake_image = io.BytesIO(b"fake png content")
        from fastapi import UploadFile

        upload_file = UploadFile(
            filename="test.png", file=fake_image, content_type="image/png"
        )

        saved_path = storage.save_image(upload_file, subfolder="test")

        assert saved_path.endswith(".png")

    def test_save_image_invalid_content_type(self, tmp_path):
        """Testa que arquivo não-imagem é rejeitado."""
        storage = FileStorage(base_path=str(tmp_path))

        fake_file = io.BytesIO(b"not an image")
        from fastapi import UploadFile

        upload_file = UploadFile(
            filename="test.pdf", file=fake_file, content_type="application/pdf"
        )

        with pytest.raises(ValueError, match="Tipo de arquivo inválido"):
            storage.save_image(upload_file, subfolder="test")

    def test_save_image_invalid_extension(self, tmp_path):
        """Testa que extensão inválida é rejeitada."""
        storage = FileStorage(base_path=str(tmp_path))

        fake_file = io.BytesIO(b"fake content")
        from fastapi import UploadFile

        upload_file = UploadFile(
            filename="test.exe", file=fake_file, content_type="image/jpeg"
        )

        with pytest.raises(ValueError, match="Extensão de arquivo inválida"):
            storage.save_image(upload_file, subfolder="test")

    def test_delete_image_existing(self, tmp_path):
        """Testa deleção de imagem existente."""
        storage = FileStorage(base_path=str(tmp_path))

        # Criar arquivo
        test_dir = tmp_path / "test"
        test_dir.mkdir()
        test_file = test_dir / "test.jpg"
        test_file.write_text("fake content")

        # Deletar
        result = storage.delete_image("/test/test.jpg")

        assert result is True
        assert not test_file.exists()

    def test_delete_image_nonexistent(self, tmp_path):
        """Testa deleção de imagem que não existe."""
        storage = FileStorage(base_path=str(tmp_path))

        result = storage.delete_image("/test/nonexistent.jpg")

        assert result is False

    def test_get_absolute_path_existing(self, tmp_path):
        """Testa obtenção de caminho absoluto de arquivo existente."""
        storage = FileStorage(base_path=str(tmp_path))

        # Criar arquivo
        test_dir = tmp_path / "test"
        test_dir.mkdir()
        test_file = test_dir / "test.jpg"
        test_file.write_text("fake content")

        # Obter caminho
        absolute_path = storage.get_absolute_path("/test/test.jpg")

        assert absolute_path is not None
        assert absolute_path.exists()
        assert str(absolute_path) == str(test_file)

    def test_get_absolute_path_nonexistent(self, tmp_path):
        """Testa obtenção de caminho para arquivo inexistente."""
        storage = FileStorage(base_path=str(tmp_path))

        absolute_path = storage.get_absolute_path("/test/nonexistent.jpg")

        assert absolute_path is None


class TestIniciativaUploadIntegration:
    """Testes de integração para upload de imagens em iniciativas."""

    @pytest.fixture
    def fake_image_file(self):
        """Fixture que cria um arquivo de imagem fake."""
        content = b"fake image content"
        return ("test_image.jpg", io.BytesIO(content), "image/jpeg")

    def test_create_iniciativa_with_image(
        self, client: TestClient, fake_image_file, auth_headers, db_session
    ):
        """Testa criação de iniciativa com upload de imagem."""
        # Criar organizador primeiro
        from app.models.organizador_model import Organizador

        org = Organizador(id="test-org", nome="Test Org")
        db_session.add(org)
        db_session.commit()

        # Preparar dados
        form_data = {
            "titulo": "Iniciativa com Imagem",
            "descricao": "Descrição da iniciativa",
            "organizador_id": "test-org",
            "link": "https://exemplo.com",
            "local": "Caxias do Sul",
            "destaque": "false",
            "horarios": json.dumps(
                [
                    {
                        "data_evento": str(date.today()),
                        "hora_inicio": "10:00:00",
                        "hora_fim": "12:00:00",
                        "tipo": "PRESENCIAL",
                    }
                ]
            ),
        }

        # Fazer requisição com arquivo
        response = client.post(
            "/iniciativas/",
            data=form_data,
            files={"imagem": fake_image_file},
            headers=auth_headers,
        )

        # Verificar resposta
        assert response.status_code == 201
        data = response.json()
        assert data["titulo"] == "Iniciativa com Imagem"
        assert data["imagem_url"].startswith("/iniciativas/")
        assert data["imagem_url"].endswith(".jpg")

        # Verificar que arquivo foi salvo
        image_path = data["imagem_url"]
        absolute_path = file_storage.get_absolute_path(image_path)
        assert absolute_path is not None
        assert absolute_path.exists()

        # Limpar - deletar arquivo criado
        file_storage.delete_image(image_path)

    def test_create_iniciativa_invalid_image_type(
        self, client: TestClient, auth_headers, db_session
    ):
        """Testa que tipo de arquivo inválido é rejeitado."""
        # Criar organizador
        from app.models.organizador_model import Organizador

        org = Organizador(id="test-org", nome="Test Org")
        db_session.add(org)
        db_session.commit()

        form_data = {
            "titulo": "Iniciativa",
            "descricao": "Descrição",
            "organizador_id": "test-org",
            "link": "https://exemplo.com",
            "destaque": "false",
            "horarios": json.dumps(
                [
                    {
                        "data_evento": str(date.today()),
                        "hora_inicio": "10:00:00",
                        "hora_fim": "12:00:00",
                        "tipo": "PRESENCIAL",
                    }
                ]
            ),
        }

        # Arquivo PDF em vez de imagem
        fake_pdf = ("test.pdf", io.BytesIO(b"fake pdf content"), "application/pdf")

        response = client.post(
            "/iniciativas/",
            data=form_data,
            files={"imagem": fake_pdf},
            headers=auth_headers,
        )

        assert response.status_code == 422
        assert "Tipo de arquivo inválido" in response.json()["detail"]

    def test_create_iniciativa_with_tags_and_image(
        self, client: TestClient, fake_image_file, auth_headers, db_session
    ):
        """Testa criação com tags e imagem."""
        from app.models.organizador_model import Organizador
        from app.models.tag_model import Tag

        # Criar organizador e tags
        org = Organizador(id="test-org", nome="Test Org")
        tag1 = Tag(id="tag-1", nome="Tag 1", descricao="Descrição 1")
        tag2 = Tag(id="tag-2", nome="Tag 2", descricao="Descrição 2")

        db_session.add_all([org, tag1, tag2])
        db_session.commit()

        form_data = {
            "titulo": "Iniciativa com Tags",
            "descricao": "Descrição",
            "organizador_id": "test-org",
            "link": "https://exemplo.com",
            "destaque": "true",
            "horarios": json.dumps(
                [
                    {
                        "data_evento": str(date.today()),
                        "hora_inicio": "14:00:00",
                        "hora_fim": "16:00:00",
                        "tipo": "ONLINE",
                    }
                ]
            ),
            "tag_ids": json.dumps(["tag-1", "tag-2"]),
            "descricoes_extras": json.dumps(
                ["Descrição extra 1", "Descrição extra 2"]
            ),
        }

        response = client.post(
            "/iniciativas/",
            data=form_data,
            files={"imagem": fake_image_file},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert len(data["tags"]) == 2
        assert len(data["descricoes_extras"]) == 2

        # Limpar
        file_storage.delete_image(data["imagem_url"])


@pytest.fixture
def auth_headers():
    """Headers de autenticação fake para testes."""
    return {"Authorization": "Bearer fake-token"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])



