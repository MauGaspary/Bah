from typing import List

from fastapi import HTTPException
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario
from app.repositories.iniciativa_repository import IniciativaRepository
from app.schemas.admin_iniciativa_schemas import IniciativaFiltersSchema
from app.schemas.iniciativa_schema import (
    IniciativaCreate,
    IniciativaListResponse,
    IniciativaResponse,
)


class IniciativaService:
    def __init__(self, db: Session, model: SentenceTransformer):
        self.repository = IniciativaRepository(db)
        self.model = model

    def create_iniciativa(
        self, iniciativa_data: IniciativaCreate, criado_por: str
    ) -> IniciativaResponse:
        if criado_por != "sistema":
            usuario_existe = (
                self.repository.db.query(Usuario)
                .filter(Usuario.id == criado_por)
                .first()
            )
            if not usuario_existe:
                raise ValueError("Usuário criador não encontrado")

        if iniciativa_data.organizador_id:
            if not self.repository.organizador_exists(iniciativa_data.organizador_id):
                raise ValueError(
                    f"Organizador não encontrado com ID: {iniciativa_data.organizador_id}"
                )
        else:
            raise ValueError("organizador_id é obrigatório")

        if iniciativa_data.tag_ids:
            existing_tags = self.repository.tags_exist(iniciativa_data.tag_ids)
            missing_tags = set(iniciativa_data.tag_ids) - set(existing_tags)
            if missing_tags:
                raise ValueError(f"Tags não encontradas: {', '.join(missing_tags)}")

        if iniciativa_data.organizador_id:
            duplicate = self.repository.check_duplicate_iniciativa(
                iniciativa_data.titulo, iniciativa_data.organizador_id
            )
            if duplicate:
                raise ValueError(
                    "Já existe uma iniciativa com este título para este organizador"
                )

        if iniciativa_data.organizador_id:
            conflicting_horarios = self.repository.check_conflicting_horarios(
                iniciativa_data.organizador_id, iniciativa_data.horarios
            )
            if conflicting_horarios:

                pass

        try:
            embedding = self.model.encode(
                iniciativa_data.descricao,
                convert_to_numpy=True,
                normalize_embeddings=True,
            )

            embeddings_descricoes_extras = []
            for description_for_search in iniciativa_data.descricoes_extras or []:
                embedding_extra = self.model.encode(
                    description_for_search,
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                )
                embeddings_descricoes_extras.append(embedding_extra)

            iniciativa = self.repository.create(
                iniciativa_data,
                criado_por,
                descricao_vetor=embedding,
                descricoes_extras_vetores=embeddings_descricoes_extras,
            )

            return IniciativaResponse.model_validate(iniciativa)

        except Exception as e:
            print(f"Erro na criação: {type(e).__name__}: {str(e)}")

            if "check constraint" in str(e).lower() or "constraint" in str(e).lower():
                raise ValueError(
                    "Dados inválidos: verifique se a hora de fim é maior que a hora de início"
                ) from e
            raise RuntimeError(f"Erro interno do servidor: {str(e)}") from e

    def get_iniciativa_by_id(self, iniciativa_id: str) -> IniciativaResponse:
        iniciativa = self.repository.get_by_id(iniciativa_id)
        if not iniciativa:
            raise ValueError("Iniciativa não encontrada")
        return IniciativaResponse.model_validate(iniciativa)

    def search_iniciativas(
        self, query: str, page: int, size: int
    ) -> IniciativaListResponse:
        embedding = self.model.encode(
            query, convert_to_numpy=True, normalize_embeddings=True
        )
        try:
            iniciativas, total = self.repository.search_by_embedding(
                embedding, page, size
            )

            filters = IniciativaFiltersSchema(q=query, page=page, size=size)
            return IniciativaListResponse(
                items=iniciativas, total=total, filters=filters
            )
        except Exception as e:
            print(f"Erro na busca: {type(e).__name__}: {str(e)}")
            raise ValueError(
                status_code=500, detail=f"Erro interno do servidor na service: {str(e)}"
            ) from e
