from fastapi import APIRouter, HTTPException, Query
import random
from collections import defaultdict
from .. import crud

router = APIRouter(
    prefix="/mundo",
    tags=["Mundo Pokémon"]
)
AREAS_DATA = {
    "1": {
        "nome": "Rota Inicial",
        "max_level": 30,
        "allowed_rarities": ["Comum", "Incomum", "Raro"]
    }
}

AREA_1_ENCOUNTER_CHANCE = {
    "Comum": 750,
    "Incomum": 200,
    "Raro": 50
}

@router.get("/encontrar-pokemon")
def encontrar_pokemon_selvagem(area: str = "1"):
    area = "1"
    if area not in AREAS_DATA:
        raise HTTPException(status_code=404, detail="Área não encontrada.")
    area_rules = AREAS_DATA[area]
    pokedex = crud.get_pokedex()
    pokemon_por_raridade = defaultdict(list)
    for pokemon in pokedex:
        raridade = pokemon.get("raridade")
        if raridade and raridade in area_rules["allowed_rarities"]:
            pokemon_por_raridade[raridade].append(pokemon)


    lista_de_raridades = list(AREA_1_ENCOUNTER_CHANCE.keys())
    pesos_das_raridades = list(AREA_1_ENCOUNTER_CHANCE.values())
    raridade_sorteada = random.choices(lista_de_raridades, weights=pesos_das_raridades, k=1)[0]
    lista_de_encontros_possiveis = pokemon_por_raridade[raridade_sorteada]
    if not lista_de_encontros_possiveis:
        lista_de_encontros_possiveis = pokemon_por_raridade["Comum"]
    pokemon_encontrado_modelo = random.choice(lista_de_encontros_possiveis)
    return pokemon_encontrado_modelo