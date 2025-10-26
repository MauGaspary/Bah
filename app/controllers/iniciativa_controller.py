from datetime import date, datetime
from typing import Optional

from fastapi import HTTPException
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from app.schemas.iniciativa_schema import (
    CalendarioMensalResponse,
    IniciativaCreate,
    IniciativaListResponseSchema,
    IniciativaPatchSchema,
    IniciativaResponse,
    IniciativaSchema,
)
from app.services.iniciativa_service import IniciativaService
from app.utils.exceptions import ResourceNotFound


class IniciativaController:

    def __init__(self, db: Session, model: Optional[SentenceTransformer] = None):
        self.service = IniciativaService(db, model)

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
        """Lista iniciativas com filtros (admin)."""
        try:
            return self.service.listar_iniciativas(
                q, created_from, created_to, order_by, order_dir, page, size
            )
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error") from e

    def delete_iniciativa(self, iniciativa_id: str, deletado_por: str) -> None:
        """Soft delete de uma iniciativa (admin)."""
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
        model: Optional[object] = None,
    ) -> IniciativaSchema:
        """
        Aplica alterações parciais em uma iniciativa (admin).
        - 404 se não existir ou estiver soft-deletada
        - 422 se regras de validação forem violadas
        - 200 (retorno) com a iniciativa atualizada
        """
        try:
            return self.service.patch_iniciativa(
                iniciativa_id=iniciativa_id,
                payload=payload,
                editado_por=editado_por,
                model=model,
            )
        except ResourceNotFound as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erro ao atualizar iniciativa: {str(e)}"
            ) from e

    def get_iniciativa_by_id_admin(self, iniciativa_id: str) -> IniciativaSchema:
        try:
            return self.service.get_iniciativa_by_id_admin(iniciativa_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail={"message": str(e)}) from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail={"message": "Erro ao buscar iniciativa"}
            ) from e

    def create_iniciativa(
        self,
        iniciativa_data: IniciativaCreate,
        criado_por: str,
    ) -> IniciativaResponse:
        try:
            return self.service.create_iniciativa(iniciativa_data, criado_por)
        except ValueError as e:
            raise HTTPException(422, str(e)) from e
        except RuntimeError as e:
            raise HTTPException(500, str(e)) from e

    def get_iniciativa_by_id(self, iniciativa_id: str) -> IniciativaResponse:
        return self.service.get_iniciativa_by_id(iniciativa_id)

    def get_calendario_mensal(self, data: date) -> CalendarioMensalResponse:
        return self.service.get_calendario_mensal(data)

    def search_iniciativas(self, query: str, page: int, size: int):
        try:
            return self.service.search_iniciativas(query, page, size)
        except HTTPException as e:
            raise e
