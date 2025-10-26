from typing import List

from sqlalchemy.orm import Session

from app.models.tag_model import Tag
from app.repositories.tag_repository import TagRepository
from app.schemas.tag_schema import TagCreate, TagResponse, TagUpdate
from app.utils.exceptions import ResourceNotFoundException


class TagService:

    def __init__(self, db: Session):
        self.repository = TagRepository(db)

    def list_all(self) -> List[TagResponse]:
        tags = self.repository.list_all()
        return [TagResponse.model_validate(tag) for tag in tags]

    def get_by_id(self, tag_id: str) -> TagResponse:
        tag = self.repository.get_by_id(tag_id)
        if not tag:
            raise ResourceNotFoundException(f"Tag com ID {tag_id} não encontrada")
        return TagResponse.model_validate(tag)

    def create(self, tag_data: TagCreate) -> TagResponse:
        tag = Tag(
            nome=tag_data.nome,
            descricao=tag_data.descricao,
        )
        created_tag = self.repository.create(tag)
        return TagResponse.model_validate(created_tag)

    def update(self, tag_id: str, tag_data: TagUpdate) -> TagResponse:
        tag = self.repository.get_by_id(tag_id)
        if not tag:
            raise ResourceNotFoundException(f"Tag com ID {tag_id} não encontrada")

        if tag_data.nome is not None:
            tag.nome = tag_data.nome
        if tag_data.descricao is not None:
            tag.descricao = tag_data.descricao

        updated_tag = self.repository.update(tag)
        return TagResponse.model_validate(updated_tag)

    def delete(self, tag_id: str) -> None:
        tag = self.repository.get_by_id(tag_id)
        if not tag:
            raise ResourceNotFoundException(f"Tag com ID {tag_id} não encontrada")
        self.repository.delete(tag)
