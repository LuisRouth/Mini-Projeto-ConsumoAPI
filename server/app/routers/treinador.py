from fastapi import APIRouter, HTTPException, Query
import random
import math
from .. import schemas, crud

router = APIRouter(
    prefix="/treinador",
    tags=["Treinadores"]
)

@router.post("", status_code=201)
def criar_treinador(treinador_data: schemas.TreinadorCreate):
    novo_treinador = crud.criar_novo_treinador(treinador_data.nome)
    return novo_treinador

@router.post("/{treinador_id}/mover-pokemon", status_code=200)
def mover(treinador_id: int, id_captura: int, de_lista: str, de_index: int, para_lista: str, para_index: int):
    resultado = crud.mover_pokemon(treinador_id, id_captura, de_lista, de_index, para_lista, para_index)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado

@router.get("/{treinador_id}/pc")
def get_pc_do_treinador(treinador_id: int):
    treinador = crud.get_treinador_by_id(treinador_id)
    if not treinador:
        raise HTTPException(status_code=404, detail="Treinador não encontrado")
    return treinador.get("pc", [])

@router.post("/{treinador_id}/escolher-inicial", status_code=201)
def escolher_inicial(treinador_id: int, escolha: schemas.EscolhaAcao):
    treinador = crud.get_treinador_by_id(treinador_id)
    if not treinador:
        raise HTTPException(status_code=404, detail="Treinador não encontrado")
    if treinador.get("equipe") or any(p is not None for p in treinador.get("pc", [])):
        raise HTTPException(status_code=400, detail="Este treinador já possui Pokémon.")

    pokemon_modelo = crud.get_pokemon_from_pokedex_by_nome(escolha.pokemon_nome)
    if not pokemon_modelo or not pokemon_modelo.get("is_inicial", False):
        raise HTTPException(status_code=400, detail="O Pokémon escolhido não é um inicial válido.")
        
    nivel_inicial = 10
    stats_iniciais = crud.calcular_stats_pokemon(pokemon_modelo, nivel_inicial)
    novo_pokemon = {
        "id_captura": crud.gerar_novo_id_captura(),
        "pokedex_id": pokemon_modelo["id"],
        "nome": pokemon_modelo["nome"],
        "nivel": nivel_inicial,
        "hp_max": stats_iniciais["hp"],
        "hp": stats_iniciais["hp"],
        "ataque": stats_iniciais["ataque"],
        "xp_atual": 0,
        "xp_para_upar": crud.calcular_xp_necessario(nivel_inicial + 1)
    }
    
    gamestate = crud.get_gamestate()
    sucesso = crud.adicionar_pokemon_ao_treinador(treinador_id, novo_pokemon, gamestate)
    
    if not sucesso:
        raise HTTPException(status_code=500, detail="Erro interno ao adicionar o Pokémon.")
    crud.save_gamestate(gamestate)
    
    return novo_pokemon

@router.post("/{treinador_id}/treinar/{id_captura}", status_code=200)
def treinar_pokemon(treinador_id: int, id_captura: int, area_atual: str = Query(..., description="O ID da área atual para determinar o level cap")):
    from . import mundo
    area_rules = mundo.AREAS_DATA.get(area_atual)
    if not area_rules:
        raise HTTPException(status_code=404, detail="Área não encontrada")
    
    level_cap = area_rules["level_range"][1]

    resultado = crud.upar_e_evoluir_pokemon(treinador_id, id_captura, level_cap)

    if "error" in resultado:
        raise HTTPException(status_code=404, detail=resultado["error"])
    
    return resultado

@router.post("/{treinador_id}/capturar", status_code=201)
def capturar_pokemon(treinador_id: int, captura: schemas.EscolhaAcao):
    treinador = crud.get_treinador_by_id(treinador_id)
    if not treinador or not treinador.get("pc"):
        raise HTTPException(status_code=400, detail="O treinador precisa de um Pokémon inicial antes de capturar.")

    pokemon_modelo = crud.get_pokemon_from_pokedex_by_nome(captura.pokemon_nome)
    if not pokemon_modelo:
        raise HTTPException(status_code=404, detail=f"Pokémon chamado '{captura.pokemon_nome}' não encontrado.")
    niveis_possiveis = list(range(10, 51, 10))
    nivel_selvagem = random.choice(niveis_possiveis)
    
    stats_captura = crud.calcular_stats_pokemon(pokemon_modelo, nivel_selvagem)

    novo_pokemon_capturado = {
        "id_captura": crud.gerar_novo_id_captura(),
        "pokedex_id": pokemon_modelo["id"],
        "nome": pokemon_modelo["nome"],
        "nivel": nivel_selvagem,
        "hp": stats_captura["hp"],
        "ataque": stats_captura["ataque"]
    }
    
    sucesso = crud.adicionar_pokemon_ao_pc(treinador_id, novo_pokemon_capturado)
    if not sucesso:
        raise HTTPException(status_code=500, detail="Erro interno ao salvar o Pokémon.")

    return novo_pokemon_capturado

@router.post("/{treinador_id}/curar", status_code=200)
def curar_pokemons(treinador_id: int):
    treinador = crud.get_treinador_by_id(treinador_id)
    if not treinador:
        raise HTTPException(status_code=404, detail="Treinador não encontrado")
    
    sucesso = crud.curar_pokemons_treinador(treinador_id)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Não foi possível curar os Pokémon.")

    return {"mensagem": "Todos os seus Pokémon foram curados!"}

@router.get("/{treinador_id}", status_code=200)
def get_treinador_completo(treinador_id: int):
    treinador = crud.get_treinador_by_id(treinador_id)
    if not treinador:
        raise HTTPException(status_code=404, detail="Treinador não encontrado")
    return treinador
    
@router.get("/{treinador_id}/equipe", status_code=200)
def get_equipe_do_treinador(treinador_id: int):
    treinador = crud.get_treinador_by_id(treinador_id)
    if not treinador:
        raise HTTPException(status_code=404, detail="Treinador não encontrado")
    return treinador.get("equipe", [])
