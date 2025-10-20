from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.admin_iniciativa_schemas import (
    IniciativaListResponseSchema,
    IniciativaPatchSchema,
    IniciativaSchema,
)
from app.services.admin_iniciativa_service import AdminIniciativaService
from app.utils.exceptions import ResourceNotFound


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
            raise HTTPException(status_code=422, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error") from e

    def delete_iniciativa(self, iniciativa_id: str, deletado_por: str) -> None:
        """Soft delete de uma iniciativa"""
        try:
            self.service.delete_iniciativa(iniciativa_id, deletado_por)
        except ValueError as e:
            raise HTTPException(status_code=404, detail={"message": str(e)}) from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Erro ao deletar iniciativa"
            ) from e

    def patch_iniciativa(
        self,
        iniciativa_id: str,
        payload: IniciativaPatchSchema,
        editado_por: Optional[str] = None,
    ) -> IniciativaSchema:
        """
        Aplica alterações parciais em uma iniciativa e retorna o objeto completo atualizado.
        - 404 se não existir ou estiver soft-deletada
        - 422 se regras de validação forem violadas
        - 200 (retorno) com a iniciativa atualizada
        """
        try:
            return self.service.patch_iniciativa(
                iniciativa_id=iniciativa_id,
                payload=payload,
                editado_por=editado_por,
            )
        except ResourceNotFound as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Erro ao atualizar iniciativa"
            ) from e

    def get_iniciativa_by_id(self, iniciativa_id: str) -> IniciativaSchema:
        try:
            return self.service.get_iniciativa_by_id(iniciativa_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail={"message": str(e)})
        except Exception as e:
            raise HTTPException(
                status_code=500, detail={"message": "Erro ao buscar iniciativa"}
            ) from e

    def get_iniciativa_by_id(self, iniciativa_id: str) -> IniciativaSchema:
        try:
            return self.service.get_iniciativa_by_id(iniciativa_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail={"message": str(e)})
        except Exception as e:
            raise HTTPException(
                status_code=500, detail={"message": "Erro ao buscar iniciativa"}
            ) from e
