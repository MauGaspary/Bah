from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.admin_iniciativa_repository import AdminIniciativaRepository
from app.schemas.admin_iniciativa_schemas import (
    IniciativaFiltersSchema,
    IniciativaListResponseSchema,
    IniciativaSchema,
)


class AdminIniciativaService:
    def __init__(self, db: Session):
        self.repository = AdminIniciativaRepository(db)

    def listar_iniciativas(
        self,
        q: Optional[str] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        order_by: str = "criado_em",
        order_dir: str = "desc",
        page: int = 1,
        size: int = 10,
    ) -> IniciativaListResponseSchema:
        if created_from and created_to and created_from > created_to:
            raise ValueError("Data inicial deve ser menor que data final")

        valid_order_fields = ["criado_em", "titulo", "destaque", "editado_em"]
        if order_by not in valid_order_fields:
            order_by = "criado_em"

        iniciativas_models = self.repository.list_iniciativas(
            q, created_from, created_to, order_by, order_dir, page, size
        )
        iniciativas = [
            IniciativaSchema.model_validate(iniciativa)
            for iniciativa in iniciativas_models
        ]

        total = self.repository.count_iniciativas(q, created_from, created_to)

        filters = IniciativaFiltersSchema(
            q=q,
            created_from=created_from,
            created_to=created_to,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
        )

        return IniciativaListResponseSchema(
            items=iniciativas, total=total, filters=filters
        )

    def delete_iniciativa(self, iniciativa_id: str, deletado_por: str = None) -> None:
        iniciativa = self.repository.soft_delete(iniciativa_id, deletado_por)
        if not iniciativa:
            raise ValueError("Iniciativa não encontrada.")
