import json
import os
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
POKEDEX_FILE = os.path.join(SCRIPT_DIR, "server", "app", "pokedex.json")

def analisar_pokedex():
    try:
        with open(POKEDEX_FILE, "r", encoding="utf-8") as f:
            pokedex_data = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo Pokedex não encontrado em '{POKEDEX_FILE}'")
        return

    contagem_raridades = defaultdict(int)
    contagem_iniciais = 0

    for pokemon in pokedex_data:
        raridade = pokemon.get("raridade", "Sem Raridade")
        contagem_raridades[raridade] += 1
        if pokemon.get("is_inicial", False):
            contagem_iniciais += 1
    
    total_pokemon = len(pokedex_data)

    print("-" * 35)
    print(" ANÁLISE DE RARIDADES DO POKEDEX")
    print("-" * 35)
    
    ordem_desejada = ["Comum", "Incomum", "Raro", "Muito Raro", "Lendário", "Mítico"]
    
    for raridade in ordem_desejada:
        if raridade in contagem_raridades:
            contagem = contagem_raridades[raridade]
            print(f"- {raridade:<12}: {contagem} Pokémon")
    
    print("-" * 35)
    print(" INFORMAÇÕES ADICIONAIS")
    print("-" * 35)
    print(f"- Pokémon Iniciais (tag): {contagem_iniciais} Pokémon")
    print("-" * 35)
    print(f" Total de Pokémon: {total_pokemon}")
    print("-" * 35)

if __name__ == "__main__":
    analisar_pokedex()