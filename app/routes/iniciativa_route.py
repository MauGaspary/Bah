from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, File, HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.model import get_embedding_model
from app.controllers.admin_iniciativa_controller import AdminIniciativaController
from app.controllers.iniciativa_controller import IniciativaController
from app.dependencies.auth import get_current_user
from app.schemas.admin_iniciativa_schemas import IniciativaListResponseSchema
from app.schemas.iniciativa_schema import IniciativaCreate, IniciativaResponse
from app.utils.image_utils import transformar_imagem_em_base64

security = HTTPBearer()

router = APIRouter()


@router.get(
    "/search",
    response_model=IniciativaListResponseSchema,
    status_code=status.HTTP_200_OK,
)
def search_iniciativas(
    q: str = Query(..., description="Texto da busca semântica"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Itens por página"),
    db: Session = Depends(get_db),
    model: SentenceTransformer = Depends(get_embedding_model),
):

    controller = IniciativaController(db, model)
    return controller.search_iniciativas(q, page, size)


@router.post(
    "/", response_model=IniciativaResponse, status_code=status.HTTP_201_CREATED
)
async def create_iniciativa(
    iniciativa: IniciativaCreate,
<<<<<<< HEAD
    file: UploadFile = File(...),
    criado_por: str = "sistema",
=======
    request: Request,
    criado_por: str = "sistema",  # TODO: Obter do token de autenticação
>>>>>>> feat/US12
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Cria uma nova iniciativa.

    Validações:
    - Todos os campos obrigatórios devem estar presentes
    - Organizador deve existir
    - Tags devem existir (se fornecidas)
    - Hora de fim deve ser maior que hora de início
    - Não deve haver duplicidade de título para o mesmo organizador

    Retorna 201 com o recurso criado ou 422 quando validações falham.
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo enviado não é uma imagem válida.",
        )

    file_content = await file.read()

    imagem_base64 = transformar_imagem_em_base64(file_content)

    iniciativa_data = iniciativa.dict()
    iniciativa_data["imagem_base64"] = imagem_base64

    controller = IniciativaController(db)
    return controller.create_iniciativa(IniciativaCreate(**iniciativa_data), criado_por)
