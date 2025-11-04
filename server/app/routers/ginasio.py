from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from .. import crud, schemas

router = APIRouter(
    prefix="/ginasio",
    tags=["Ginásios"]
)

class DesafioRequest(BaseModel):
    treinador_id: int

@router.post("/{ginasio_id}/desafiar")
def desafiar_lider_de_ginasio(ginasio_id: str, treinador_id: int = Body(..., embed=True)):
    treinador = crud.get_treinador_by_id(treinador_id)
    if not treinador:
        raise HTTPException(status_code=404, detail="Treinador não encontrado.")
    nova_batalha_ginasio = crud.criar_batalha_de_ginasio(treinador, ginasio_id)
    
    if "error" in nova_batalha_ginasio:
        raise HTTPException(status_code=400, detail=nova_batalha_ginasio["error"])
        
    return nova_batalha_ginasio

@router.post("/batalha/{batalha_id}/acao")
def acao_batalha_ginasio(batalha_id: int, acao: schemas.AcaoBatalha):
    resultado_acao = crud.processar_acao_batalha_ginasio(batalha_id, acao)
    
    if "error" in resultado_acao:
        raise HTTPException(status_code=400, detail=resultado_acao["error"])
        
    return resultado_acao