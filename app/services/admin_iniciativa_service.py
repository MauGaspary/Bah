from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.repositories.admin_iniciativa_repository import AdminIniciativaRepository
from app.schemas.admin_iniciativa_schemas import IniciativaListResponseSchema, IniciativaFiltersSchema


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
 
        valid_order_fields = ["criado_em", "titulo", "destaque", "editado_em"]
        if order_by not in valid_order_fields:
            order_by = "criado_em"
        
        try:
       
            iniciativas = self.repository.list_iniciativas(
                q, created_from, created_to, order_by, order_dir, page, size
            )
            
   
            total = self.repository.count_iniciativas(
                q, created_from, created_to
            )
        except Exception:
  
            iniciativas = []
            total = 0


        filters = IniciativaFiltersSchema(
            q=q,
            created_from=created_from,
            created_to=created_to,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size
        )

        return IniciativaListResponseSchema(
            items=iniciativas,
            total=total,
            filters=filters
        )