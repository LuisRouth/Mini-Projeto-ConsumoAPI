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

@router.post("/batalha/{batalha_id}/trocar")
def trocar_pokemon_batalha_ginasio(batalha_id: int, acao: schemas.AcaoTroca):
    batalha = crud.get_batalha_by_id(batalha_id)
    # Validações para garantir a segurança da ação
    if not batalha or batalha.get("tipo") != "GINASIO":
        raise HTTPException(status_code=404, detail="Batalha de ginásio não encontrada.")
        
    treinador = crud.get_treinador_by_id(batalha["treinador_id"])
    pokemon_para_trocar = crud.get_pokemon_da_equipe_by_id(treinador["id"], acao.id_captura_para_troca)
    
    if not pokemon_para_trocar:
        raise HTTPException(status_code=404, detail="Pokémon escolhido para troca não foi encontrado.")
    if pokemon_para_trocar["hp"] <= 0:
        raise HTTPException(status_code=400, detail="Você não pode trocar para um Pokémon desmaiado!")
    if pokemon_para_trocar["id_captura"] == batalha["pokemon_em_campo_id_captura"]:
        raise HTTPException(status_code=400, detail="Este Pokémon já está em batalha!")
    
    # Chama a função principal do crud (que criaremos a seguir)
    batalha_atualizada = crud.processar_troca_pokemon_ginasio(batalha, pokemon_para_trocar)
    return batalha_atualizada