from datetime import datetime
from typing import List, Optional, cast

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.model import get_embedding_model
from app.controllers.iniciativa_controller import IniciativaController
from app.dependencies.auth import get_current_user
from app.schemas.iniciativa_schema import (
    IniciativaCreate,
    IniciativaHorarioCreate,
    IniciativaListResponseSchema,
    IniciativaPatchSchema,
    IniciativaSchema,
)

router = APIRouter()


@router.post(
    "/",
    response_model=IniciativaSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_iniciativa(
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
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    model: Optional[object] = Depends(get_embedding_model),
):
    """Cria uma nova iniciativa (admin). Aceita arquivo ou URL para imagem."""
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
        
        controller = IniciativaController(db, cast(Optional[SentenceTransformer], model))
        created = controller.create_iniciativa(iniciativa_data, current_user)
        return controller.get_iniciativa_by_id_admin(created.id)
    except Exception as e:
        # Se houver erro e fizemos upload, deletar a imagem
        if imagem and final_imagem_url:
            file_storage.delete_image(final_imagem_url)
        raise e


@router.get("/{iniciativa_id}", response_model=IniciativaSchema)
def get_iniciativa_by_id(
    iniciativa_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Busca uma iniciativa pelo ID."""
    controller = IniciativaController(db, None)
    return controller.get_iniciativa_by_id_admin(iniciativa_id)


@router.get("/", response_model=IniciativaListResponseSchema)
def listar_iniciativas(
    q: Optional[str] = Query(None, description="Busca por titulo, descricao ou tags"),
    created_from: Optional[datetime] = Query(
        None, description="Data de criacao inicial (YYYY-MM-DD)"
    ),
    created_to: Optional[datetime] = Query(
        None, description="Data de criacao final (YYYY-MM-DD)"
    ),
    order_by: str = Query(
        "criado_em",
        description="Campo para ordenacao",
        pattern="^(criado_em|titulo|destaque|editado_em)$",
    ),
    order_dir: str = Query(
        "desc", description="Direcao da ordenacao", pattern="^(asc|desc)$"
    ),
    page: int = Query(1, ge=1, description="Numero da pagina"),
    size: int = Query(10, ge=1, le=100, description="Itens por pagina"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    controller = IniciativaController(db, None)
    return controller.listar_iniciativas(
        q, created_from, created_to, order_by, order_dir, page, size
    )


@router.delete("/{iniciativa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_iniciativa(
    iniciativa_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """
    Soft delete de uma iniciativa (marca deletado_em e deletado_por)
    - Idempotente: múltiplas chamadas retornam 204
    - Retorna 404 se a iniciativa não existir
    """
    controller = IniciativaController(db, None)
    controller.delete_iniciativa(iniciativa_id, current_user)


@router.patch(
    "/{iniciativa_id}",
    response_model=IniciativaSchema,
    status_code=status.HTTP_200_OK,
)
async def patch_iniciativa(
    iniciativa_id: str,
    titulo: Optional[str] = Form(None),
    descricao: Optional[str] = Form(None),
    organizador_id: Optional[str] = Form(None),
    link: Optional[str] = Form(None),
    local: Optional[str] = Form(None),
    imagem_url: Optional[str] = Form(None),
    imagem: Optional[UploadFile] = File(None),
    destaque: Optional[bool] = Form(None),
    horarios: Optional[str] = Form(None),  # JSON string
    tag_ids: Optional[str] = Form(None),  # JSON string (tags_ids no schema)
    descricoes_extras_update: Optional[str] = Form(None),  # JSON string
    descricoes_extras_delete_ids: Optional[str] = Form(None),  # JSON string
    descricoes_extras_add: Optional[str] = Form(None),  # JSON string
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    model: Optional[object] = Depends(get_embedding_model),
):
    """Atualiza parcialmente uma iniciativa existente.
    - 404 se não existir/soft-deletada
    - 422 se violar regras de validação
    - 200 com objeto completo atualizado
    """
    import json
    from fastapi import HTTPException
    from app.utils.file_storage import file_storage
    
    # Processar upload de imagem se fornecido
    final_imagem_url = imagem_url
    if imagem:
        try:
            final_imagem_url = file_storage.save_image(imagem, subfolder="iniciativas")
        except ValueError as e:
            raise HTTPException(422, f"Erro ao processar imagem: {str(e)}")
        except Exception as e:
            raise HTTPException(500, f"Erro ao salvar imagem: {str(e)}")
    
    # Construir payload do IniciativaPatchSchema
    try:
        payload_dict = {}
        
        if titulo is not None:
            payload_dict['titulo'] = titulo
        if descricao is not None:
            payload_dict['descricao'] = descricao
        if organizador_id is not None:
            payload_dict['organizador_id'] = organizador_id
        if link is not None:
            payload_dict['link'] = link
        if local is not None:
            payload_dict['local'] = local
        if final_imagem_url is not None:
            payload_dict['imagem_url'] = final_imagem_url
        if destaque is not None:
            payload_dict['destaque'] = destaque
        
        # Parse JSON fields
        if horarios is not None:
            payload_dict['horarios'] = json.loads(horarios)
        if tag_ids is not None:
            payload_dict['tags_ids'] = json.loads(tag_ids)
        if descricoes_extras_update is not None:
            payload_dict['descricoes_extras_update'] = json.loads(descricoes_extras_update)
        if descricoes_extras_delete_ids is not None:
            payload_dict['descricoes_extras_delete_ids'] = json.loads(descricoes_extras_delete_ids)
        if descricoes_extras_add is not None:
            payload_dict['descricoes_extras_add'] = json.loads(descricoes_extras_add)
        
        # Criar IniciativaPatchSchema
        from app.schemas.iniciativa_schema import IniciativaPatchSchema
        payload = IniciativaPatchSchema(**payload_dict)
        
        controller = IniciativaController(db, cast(Optional[SentenceTransformer], model))
        return controller.patch_iniciativa(
            iniciativa_id=iniciativa_id,
            payload=payload,
            editado_por=current_user,
            model=model,
        )
    except Exception as e:
        # Se houver erro e fizemos upload, deletar a imagem
        if imagem and final_imagem_url:
            file_storage.delete_image(final_imagem_url)
        raise e
