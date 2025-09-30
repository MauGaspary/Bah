from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.admin_iniciativa_schemas import (
    IniciativaListResponseSchema,
    IniciativaSchema,
    IniciativaUpdateSchema,
)
from app.services.admin_iniciativa_service import AdminIniciativaService


class AdminIniciativaController:
    def __init__(self, db: Session):
        self.service = AdminIniciativaService(db)

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
        try:
            return self.service.listar_iniciativas(
                q, created_from, created_to, order_by, order_dir, page, size
            )
        except ValueError as e:
            raise HTTPException(
                status_code=422, detail={"fieldErrors": {"general": str(e)}}
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail={"message": "Internal server error"}
            ) from e

    def editar_iniciativa(
        self, iniciativa_id: str, dados: IniciativaUpdateSchema, editado_por: str
    ) -> IniciativaSchema:
        try:
            return self.service.editar_iniciativa(iniciativa_id, dados, editado_por)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail={"message": "Internal server error"}
            ) from e

    def delete_iniciativa(self, iniciativa_id: str, deletado_por: str = None) -> None:
        """Soft delete de uma iniciativa"""
        try:
            return self.service.delete_iniciativa(iniciativa_id, deletado_por)
        except ValueError as e:
            raise HTTPException(status_code=404, detail={"message": str(e)})
        except Exception as e:
            raise HTTPException(
                status_code=500, detail={"message": "Erro ao deletar iniciativa"}
            ) from e
