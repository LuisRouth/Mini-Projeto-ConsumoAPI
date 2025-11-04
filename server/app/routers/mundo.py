from fastapi import APIRouter, HTTPException
import random
from collections import defaultdict
from .. import crud

router = APIRouter(
    prefix="/mundo",
    tags=["Mundo Pokémon"]
)

# --- ESTRUTURA DE DADOS COMPLETA PARA TODAS AS ÁREAS ---
AREAS_DATA = {
    "1": {
        "nome": "Rota Inicial",
        "level_range": (10, 30),
        "allowed_rarities": ["Comum", "Incomum", "Raro"],
        "encounter_chance": {"Comum": 750, "Incomum": 200, "Raro": 50},
        "xp_multiplier": 1.0
    },
    "2": {
        "nome": "Floresta Sombria",
        "level_range": (30, 50),
        "allowed_rarities": ["Incomum", "Raro", "Muito Raro"],
        "encounter_chance": {"Incomum": 700, "Raro": 350, "Muito Raro": 40},
        "xp_multiplier": 2.0
    },
    "3": {
        "nome": "Montanhas Rochosas",
        "level_range": (50, 80),
        "allowed_rarities": ["Raro", "Muito Raro", "Mítico"],
        "encounter_chance": {"Raro": 600, "Muito Raro": 300, "Mítico": 30},
        "xp_multiplier": 4.0
    },
    "4": {
        "nome": "Caverna Misteriosa",
        "level_range": (80, 100),
        "allowed_rarities": ["Muito Raro", "Mítico", "Lendário"],
        "encounter_chance": {"Muito Raro": 400, "Mítico": 300, "Lendário": 70},
        "xp_multiplier": 8.0
    }
}

# --- AQUI ESTÁ O ENDPOINT QUE ESTAVA FALTANDO ---
@router.get("/areas")
def get_todas_as_areas():
    """Retorna as informações básicas de todas as áreas exploráveis."""
    return AREAS_DATA

# --- FUNÇÃO ATUALIZADA PARA USAR AS NOVAS REGRAS ---
@router.get("/encontrar-pokemon")
def encontrar_pokemon_selvagem(area_id: str = "1"):
    if area_id not in AREAS_DATA:
        raise HTTPException(status_code=404, detail="Área não encontrada.")
    
    area_rules = AREAS_DATA[area_id]
    pokedex = crud.get_pokedex()
    pokemon_por_raridade = defaultdict(list)
    for pokemon in pokedex:
        raridade = pokemon.get("raridade")
        if raridade and raridade in area_rules["allowed_rarities"]:
            pokemon_por_raridade[raridade].append(pokemon)

    lista_de_raridades = list(area_rules["encounter_chance"].keys())
    pesos_das_raridades = list(area_rules["encounter_chance"].values())
    
    raridade_sorteada = random.choices(lista_de_raridades, weights=pesos_das_raridades, k=1)[0]
    
    lista_de_encontros_possiveis = pokemon_por_raridade[raridade_sorteada]
    if not lista_de_encontros_possiveis:
        raise HTTPException(status_code=500, detail=f"Nenhum Pokémon com raridade '{raridade_sorteada}' encontrado para esta área.")

    pokemon_encontrado_modelo = random.choice(lista_de_encontros_possiveis).copy()

    min_level, max_level = area_rules["level_range"]
    nivel_encontrado = random.randint(min_level, max_level)
    pokemon_encontrado_modelo['nivel'] = nivel_encontrado
    
    return pokemon_encontrado_modelo