from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.admin_iniciativa_schemas import IniciativaListResponseSchema
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
            if created_from and created_to and created_from > created_to:
                raise HTTPException(
                    status_code=422,
                    detail={
                        "fieldErrors": {
                            "created_from": "Data inicial deve ser menor que data final"
                        }
                    },
                )

            return self.service.listar_iniciativas(
                q, created_from, created_to, order_by, order_dir, page, size
            )
        except HTTPException:

            raise
        except ValueError as e:
            raise HTTPException(
                status_code=422, detail={"fieldErrors": {"general": str(e)}}
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail={"message": "Internal server error"}
            ) from e
