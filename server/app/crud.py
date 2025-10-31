import random
import math
import json
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
POKEDEX_FILE = os.path.join(APP_DIR, "pokedex.json")
GAMESTATE_FILE = os.path.join(APP_DIR, "gamestate.json")

RARITY_MULTIPLIERS = {
    "Comum": 1.0,
    "Incomum": 1.1,
    "Raro": 1.25,
    "Muito Raro": 1.4,
    "Lendário": 1.5,
    "Mítico": 1.6
}

def get_pokedex():
    with open(POKEDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_gamestate():
    try:
        with open(GAMESTATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"treinadores": []}
    
def save_gamestate(data: dict):
    with open(GAMESTATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_treinador_by_id(treinador_id: int):
    gamestate = get_gamestate()
    for t in gamestate.get("treinadores", []):
        if t["id"] == treinador_id:
            return t
    return None

def get_iniciais_from_pokedex():
    pokedex = get_pokedex()
    return [p for p in pokedex if p.get("is_inicial")]

def get_pokemon_from_pokedex_by_nome(pokemon_nome: str):
    pokedex = get_pokedex()
    for p in pokedex:
        if p["nome"].lower() == pokemon_nome.lower():
            return p
    return None

def gerar_novo_id_captura() -> int:
    gamestate = get_gamestate()
    max_id = 0
    for treinador in gamestate.get("treinadores", []):
        for pokemon in treinador.get("pc", []):
            if pokemon["id_captura"] > max_id:
                max_id = pokemon["id_captura"]
    return max_id + 1

def calcular_stats_pokemon(pokemon_modelo: dict, nivel: int) -> dict:
    raridade = pokemon_modelo.get("raridade", "Comum")
    multiplicador = RARITY_MULTIPLIERS.get(raridade, 1.0)
    
    stats_base = pokemon_modelo["stats_base"]
    
    hp_calculado = math.floor((stats_base["hp"] + (nivel * 1.5)) * multiplicador)
    ataque_calculado = math.floor((stats_base["ataque"] + nivel) * multiplicador)
    
    return {"hp": hp_calculado, "ataque": ataque_calculado}

def criar_novo_treinador(nome_treinador: str) -> dict:
    gamestate = get_gamestate()
    treinadores = gamestate.get("treinadores", [])
    novo_id = 1
    if treinadores:
        novo_id = max(t["id"] for t in treinadores) + 1
    novo_treinador = {"id": novo_id, "nome": nome_treinador, "pc": []}
    treinadores.append(novo_treinador)
    save_gamestate(gamestate)
    return novo_treinador

def adicionar_pokemon_ao_pc(treinador_id: int, novo_pokemon: dict) -> bool:
    gamestate = get_gamestate()
    treinadores = gamestate.get("treinadores", [])
    
    treinador_encontrado = False
    for t in treinadores:
        if t["id"] == treinador_id:
            t["pc"].append(novo_pokemon)
            treinador_encontrado = True
            break
            
    if not treinador_encontrado:
        return False 
    save_gamestate(gamestate)
    return True

def get_pokemon_do_pc_by_id(treinador_id: int, id_captura: int):
    treinador = get_treinador_by_id(treinador_id)
    if not treinador: return None
    for p in treinador.get("pc", []):
        if p["id_captura"] == id_captura:
            return p
    return None

def atualizar_pokemon_no_pc(treinador_id: int, pokemon_atualizado: dict):
    gamestate = get_gamestate()
    for t in gamestate.get("treinadores", []):
        if t["id"] == treinador_id:
            for i, p in enumerate(t["pc"]):
                if p["id_captura"] == pokemon_atualizado["id_captura"]:
                    t["pc"][i] = pokemon_atualizado
                    save_gamestate(gamestate)
                    return True
    return False

def _gerar_novo_id_batalha(gamestate: dict) -> int:
    max_id = 0
    for batalha in gamestate.get("batalhas_ativas", []):
        if batalha["id"] > max_id:
            max_id = batalha["id"]
    return max_id + 1

def criar_nova_batalha(treinador: dict, pokemon_treinador: dict, pokemon_selvagem_modelo: dict) -> dict:

    gamestate = get_gamestate()
    nivel_base_jogador = pokemon_treinador['nivel']
    nivel_selvagem = max(1, nivel_base_jogador + random.randint(-5, 5))

    stats_oponente = calcular_stats_pokemon(pokemon_selvagem_modelo, nivel_selvagem)

    oponente = {
        "pokedex_id": pokemon_selvagem_modelo["id"],
        "nome": pokemon_selvagem_modelo["nome"],
        "nivel": nivel_selvagem,
        "hp_max": stats_oponente["hp"],
        "hp_atual": stats_oponente["hp"],
        "ataque": stats_oponente["ataque"]
    }

    nova_batalha = {
        "id": _gerar_novo_id_batalha(gamestate),
        "treinador_id": treinador["id"],
        "pokemon_em_campo_id_captura": pokemon_treinador["id_captura"], # Agora funciona!
        "oponente": oponente,
        "log_batalha": [f"Um {oponente['nome']} selvagem (Nível {nivel_selvagem}) apareceu!"]
    }

    gamestate.setdefault("batalhas_ativas", []).append(nova_batalha)
    save_gamestate(gamestate)

    return nova_batalha

def get_batalha_by_id(batalha_id: int):
    gamestate = get_gamestate()
    for b in gamestate.get("batalhas_ativas", []):
        if b["id"] == batalha_id:
            return b
    return None

def deletar_batalha(batalha_id: int):
    gamestate = get_gamestate()
    batalhas = gamestate.get("batalhas_ativas", [])
    batalhas_filtradas = [b for b in batalhas if b["id"] != batalha_id]
    gamestate["batalhas_ativas"] = batalhas_filtradas
    save_gamestate(gamestate)

def get_pokemon_from_pokedex_by_id(pokedex_id: int):
    pokedex = get_pokedex()
    for p in pokedex:
        if p["id"] == pokedex_id:
            return p
    return None