from sqlalchemy.orm import Session
from typing import Dict
from app.repositories.admin_iniciativa_repository import AdminIniciativaRepository


class AdminIniciativaService:

    @staticmethod
    def listar_iniciativas(
        db: Session,
        q: str = None,
        created_from: str = None,
        created_to: str = None,
        order_by: str = "criado_em",
        order_dir: str = "desc",
        page: int = 1,
        size: int = 10,
    ) -> Dict:
        iniciativas = AdminIniciativaRepository.list_iniciativas(
            db, q, created_from, created_to, order_by, order_dir, page, size
        )
        total = AdminIniciativaRepository.count_iniciativas(db)

        return {
            "items": iniciativas,
            "total": total,
            "filters": {
                "q": q,
                "created_from": created_from,
                "created_to": created_to,
                "order_by": order_by,
                "order_dir": order_dir,
                "page": page,
                "size": size,
            },
        }
