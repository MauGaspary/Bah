from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.model import get_embedding_model
from app.controllers.iniciativa_controller import IniciativaController
from app.schemas.iniciativa_schema import (
    CalendarioMensalResponse,
    IniciativaCreate,
    IniciativaHorarioCreate,
    IniciativaListResponse,
    IniciativaResponse,
)

security = HTTPBearer()

router = APIRouter()


@router.get(
    "/search",
    response_model=IniciativaListResponse,
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
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(...),
    organizador_id: str = Form(...),
    link: str = Form(...),
    local: Optional[str] = Form(None),
    imagem_url: Optional[str] = Form(None),
    imagem: Optional[UploadFile] = File(None),
    destaque: bool = Form(False),
    horarios: str = Form(...),  # JSON string
    tag_ids: Optional[str] = Form(None),  # JSON string
    descricoes_extras: Optional[str] = Form(None),  # JSON string
    criado_por: str = "sistema",  # TODO: Obter do token de autenticação
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Cria uma nova iniciativa.

    Validações:
    - Todos os campos obrigatórios devem estar presentes
    - Deve fornecer imagem (arquivo) OU imagem_url (string)
    - Se imagem for arquivo, deve ser válido (jpg, png, gif, webp)
    - Organizador deve existir
    - Tags devem existir (se fornecidas)
    - Hora de fim deve ser maior que hora de início
    - Não deve haver duplicidade de título para o mesmo organizador

    Retorna 201 com o recurso criado ou 422 quando validações falham.
    """
    import json
    from fastapi import HTTPException
    from app.utils.file_storage import file_storage
    
    # Validar que pelo menos uma forma de imagem foi fornecida
    if not imagem and not imagem_url:
        raise HTTPException(422, "Deve fornecer 'imagem' (arquivo) ou 'imagem_url' (string)")
    
    # Se arquivo foi enviado, fazer upload
    final_imagem_url = imagem_url
    if imagem:
        try:
            final_imagem_url = file_storage.save_image(imagem, subfolder="iniciativas")
        except ValueError as e:
            raise HTTPException(422, f"Erro ao processar imagem: {str(e)}")
        except Exception as e:
            raise HTTPException(500, f"Erro ao salvar imagem: {str(e)}")
    
    # Parse JSON fields
    horarios_data = json.loads(horarios)
    tag_ids_list = json.loads(tag_ids) if tag_ids else None
    descricoes_extras_list = json.loads(descricoes_extras) if descricoes_extras else None
    
    # Criar schema IniciativaCreate
    horarios_parsed = [IniciativaHorarioCreate(**h) for h in horarios_data]
    
    try:
        iniciativa_data = IniciativaCreate(
            titulo=titulo,
            descricao=descricao,
            organizador_id=organizador_id,
            link=link,
            local=local,
            imagem_url=final_imagem_url,
            destaque=destaque,
            horarios=horarios_parsed,
            tag_ids=tag_ids_list,
            descricoes_extras=descricoes_extras_list,
        )
        
        model = request.app.state.embedding_model
        controller = IniciativaController(db, model)
        return controller.create_iniciativa(iniciativa_data, criado_por)
    except Exception as e:
        # Se houver erro e fizemos upload, deletar a imagem
        if imagem and final_imagem_url:
            file_storage.delete_image(final_imagem_url)
        raise e


@router.get("/calendario", response_model=CalendarioMensalResponse)
def get_calendario_mensal(
    data: date = Query(..., description="Data de referência para o mês (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """
    Retorna o calendário de iniciativas para o mês especificado.

    Parâmetros:
    - data: Data de referência (qualquer dia do mês desejado)

    Retorna:
    - Lista de dias do mês com iniciativas agrupadas por dia
    - Iniciativas ordenadas por horário e título
    - Dias sem iniciativas retornam lista vazia
    """

    controller = IniciativaController(db)
    return controller.get_calendario_mensal(data)


@router.get("/{iniciativa_id}", response_model=IniciativaResponse)
def get_iniciativa_by_id(
    iniciativa_id: str,
    db: Session = Depends(get_db),
):
    """Busca uma iniciativa pelo ID."""
    controller = IniciativaController(db)
    return controller.get_iniciativa_by_id(iniciativa_id)
