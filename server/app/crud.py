import random
import math
import json
import os
from .routers import mundo
from . import schemas, type_logic

APP_DIR = os.path.dirname(os.path.abspath(__file__))
POKEDEX_FILE = os.path.join(APP_DIR, "pokedex.json")
GAMESTATE_FILE = os.path.join(APP_DIR, "gamestate.json")
GINASIOS_FILE = os.path.join(APP_DIR, "ginasios.json")

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

def get_pokemon_da_equipe_by_id(treinador_id: int, id_captura: int):
    treinador = get_treinador_by_id(treinador_id)
    if not treinador: return None
    for p in treinador.get("equipe", []):
        if p["id_captura"] == id_captura:
            return p
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
        todos_os_pokemon = treinador.get("equipe", []) + treinador.get("pc", [])
        for pokemon in todos_os_pokemon:
            if pokemon: 
                if pokemon["id_captura"] > max_id:
                    max_id = pokemon["id_captura"]
            
    return max_id + 1

def calcular_xp_necessario(nivel: int) -> int:
    if nivel <= 1:
        return 0
    return math.floor((4 * (nivel ** 3) / 12)/ 6)

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
    novo_id = 1 if not treinadores else max(t["id"] for t in treinadores) + 1
    novo_treinador = {
        "id": novo_id, "nome": nome_treinador, "equipe": [],
        "pc": [None] * 30,
        "ginasios_vencidos": 0
    }
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

def adicionar_pokemon_ao_treinador(treinador_id: int, novo_pokemon: dict, gamestate: dict) -> bool:
    for t in gamestate.get("treinadores", []):
        if t["id"] == treinador_id:
            equipe_real = [p for p in t.get("equipe", []) if p is not None]
            if len(equipe_real) < 6:
                try:
                    idx_vazio = t["equipe"].index(None)
                    t["equipe"][idx_vazio] = novo_pokemon
                except (ValueError, KeyError):
                    t.setdefault("equipe", []).append(novo_pokemon)
            else:
                try:
                    primeiro_slot_vazio = t["pc"].index(None)
                    t["pc"][primeiro_slot_vazio] = novo_pokemon
                except ValueError:
                    print("PC está cheio!")
            return True
    return False

def atualizar_pokemon_na_equipe(treinador_id: int, pokemon_atualizado: dict, gamestate: dict):
    for t in gamestate.get("treinadores", []):
        if t["id"] == treinador_id:
            for i, p in enumerate(t["equipe"]):
                if p and p["id_captura"] == pokemon_atualizado["id_captura"]:
                    t["equipe"][i] = pokemon_atualizado
                    return True
    return False

def dar_xp_e_evoluir_equipe(batalha: dict, oponente_vencido: dict, gamestate: dict) -> list[str]:
    treinador_id = batalha['treinador_id']
    treinador = next((t for t in gamestate.get("treinadores", []) if t["id"] == treinador_id), None)

    if not treinador: 
        return ["Erro: Treinador não encontrado."]
    area_id = str(batalha.get("area_id", "1"))
    
    from .routers import mundo
    area_rules = mundo.AREAS_DATA.get(area_id, mundo.AREAS_DATA["1"])
    level_cap = area_rules["level_range"][1]
    xp_multiplier = area_rules.get("xp_multiplier", 1.0)

    nivel_oponente = oponente_vencido['nivel']
    fator_base = 25
    xp_ganho_base = 0
    if nivel_oponente >= 20:
        xp_ganho_base = math.floor(nivel_oponente * fator_base * 6)
    else:
        xp_ganho_base = math.floor(nivel_oponente * fator_base)
    xp_ganho_final = math.floor(xp_ganho_base * xp_multiplier)
    
    logs_gerais = [f"Todos na equipe ganharam uns absurdos {xp_ganho_final} pontos de experiência!"]
    for pokemon in treinador.get("equipe", []):
        if not pokemon or pokemon['hp'] <= 0:
            continue

        if pokemon['nivel'] >= level_cap:
            logs_gerais.append(f"{pokemon['nome']} já está no nível máximo da área e não ganhou XP.")
            continue

        pokemon['xp_atual'] += xp_ganho_final
        
        leveled_up = False
        info_pokedex_atual = get_pokemon_from_pokedex_by_id(pokemon["pokedex_id"])

        while pokemon['xp_para_upar'] > 0 and pokemon['xp_atual'] >= pokemon['xp_para_upar']:
            if pokemon['nivel'] >= level_cap:
                logs_gerais.append(f"{pokemon['nome']} atingiu o nível máximo para esta área!")
                break

            leveled_up = True
            xp_excedente = pokemon['xp_atual'] - pokemon['xp_para_upar']
            
            pokemon['nivel'] += 1
            pokemon['xp_atual'] = xp_excedente
            logs_gerais.append(f"{pokemon['nome']} subiu para o nível {pokemon['nivel']}!")
            pokemon['xp_para_upar'] = calcular_xp_necessario(pokemon['nivel'] + 1)
            
            evolucao_data = info_pokedex_atual.get("evolucao")
    
            if evolucao_data and pokemon['nivel'] >= evolucao_data.get("nivel_evolucao", 999):
                id_nova_forma = evolucao_data["evolui_para_id"]
                nova_forma_info = get_pokemon_from_pokedex_by_id(id_nova_forma)
                
                nome_antigo = pokemon['nome']
                pokemon["pokedex_id"] = nova_forma_info["id"]
                pokemon["nome"] = nova_forma_info["nome"]
                logs_gerais.append(f"O que? {nome_antigo} está evoluindo! ... Parabéns! Seu Pokémon evoluiu para {nova_forma_info['nome']}!")
                
                info_pokedex_atual = nova_forma_info
        
        if leveled_up:
            stats_novos = calcular_stats_pokemon(info_pokedex_atual, pokemon['nivel'])
            pokemon['hp_max'] = stats_novos['hp']
            pokemon['hp'] = stats_novos['hp']
            pokemon['ataque'] = stats_novos['ataque']
    
    return logs_gerais

def upar_e_evoluir_pokemon(treinador_id: int, id_captura: int, level_cap: int) -> dict:
    treinador = get_treinador_by_id(treinador_id)
    if not treinador: return {"error": "Treinador não encontrado"}
    pokemon_para_upar = None
    for p in treinador.get("equipe", []):
        if p["id_captura"] == id_captura:
            pokemon_para_upar = p
            break
    
    if not pokemon_para_upar: return {"error": "Pokémon não encontrado na equipe"}

    # LÓGICA DE UPAR DE NÍVEL
    nivel_antigo = pokemon_para_upar["nivel"]
    if nivel_antigo >= level_cap:
        return {"mensagem": f"{pokemon_para_upar['nome']} já atingiu o nível máximo da área!", "pokemon": pokemon_para_upar}
        
    nivel_novo = min(nivel_antigo + 10, level_cap)
    pokemon_para_upar["nivel"] = nivel_novo
    
    log_evolucao = ""

    # LÓGICA DE EVOLUÇÃO
    info_pokedex = get_pokemon_from_pokedex_by_id(pokemon_para_upar["pokedex_id"])
    evolucao_data = info_pokedex.get("evolucao")
    
    if evolucao_data and nivel_novo >= evolucao_data.get("nivel_evolucao", 999):
        id_nova_forma = evolucao_data["evolui_para_id"]
        nova_forma_info = get_pokemon_from_pokedex_by_id(id_nova_forma)
        
        log_evolucao = f"O que? {pokemon_para_upar['nome']} está evoluindo! ... Parabéns! Seu Pokémon evoluiu para {nova_forma_info['nome']}!"
        
        pokemon_para_upar["pokedex_id"] = nova_forma_info["id"]
        pokemon_para_upar["nome"] = nova_forma_info["nome"]
        
        info_pokedex = nova_forma_info

    # RECALCULAR STATS
    stats_novos = calcular_stats_pokemon(info_pokedex, nivel_novo)
    pokemon_para_upar["hp_max"] = stats_novos["hp"]
    pokemon_para_upar["hp"] = stats_novos["hp"]
    pokemon_para_upar["ataque"] = stats_novos["ataque"]
    
    atualizar_pokemon_na_equipe(treinador_id, pokemon_para_upar)

    return {"mensagem": log_evolucao or f"{pokemon_para_upar['nome']} subiu para o nível {nivel_novo}!", "pokemon": pokemon_para_upar}

def get_pokemon_do_pc_by_id(treinador_id: int, id_captura: int):
    treinador = get_treinador_by_id(treinador_id)
    if not treinador: return None
    for p in treinador.get("pc", []):
        if p["id_captura"] == id_captura:
            return p
    return None

def mover_pokemon(treinador_id: int, id_captura: int, de_lista: str, de_index: int, para_lista: str, para_index: int) -> dict:
    gamestate = get_gamestate()
    treinador = None
    for t in gamestate.get("treinadores", []):
        if t["id"] == treinador_id:
            treinador = t
            break
    
    if not treinador:
        return {"error": "Treinador não encontrado."}
    lista_origem = treinador.get(de_lista)
    lista_destino = treinador.get(para_lista)

    if de_index >= len(lista_origem) or para_index >= len(lista_destino):
        return {"error": "Índice de movimento inválido."}

    pokemon_origem = lista_origem[de_index]
    pokemon_destino = lista_destino[para_index]
    if not pokemon_origem or pokemon_origem['id_captura'] != id_captura:
        return {"error": "Conflito de estado. Tente novamente."}
    if de_lista == "equipe" and para_lista == "pc" and sum(1 for p in treinador["equipe"] if p) <= 1:
        return {"error": "Você não pode remover o último Pokémon da sua equipe!"}
    
    if de_lista == "pc" and para_lista == "equipe" and sum(1 for p in treinador["equipe"] if p) >= 6:
        if pokemon_destino is None:
            return {"error": "Sua equipe já está cheia!"}
    lista_destino[para_index] = pokemon_origem
    lista_origem[de_index] = pokemon_destino
    save_gamestate(gamestate)
    
    return {"mensagem": "Pokémon movido com sucesso."}

def atualizar_pokemon_no_pc(treinador_id: int, pokemon_atualizado: dict):
    gamestate = get_gamestate()
    for t in gamestate.get("treinadores", []):
        if t["id"] == treinador_id:
            for i, p in enumerate(t["pc"]):
                if p is not None and p["id_captura"] == pokemon_atualizado["id_captura"]:
                    t["pc"][i] = pokemon_atualizado
                    save_gamestate(gamestate)
                    return True
    return False

def atualizar_batalha(batalha_atualizada: dict, gamestate: dict):
    batalhas = gamestate.get("batalhas_ativas", [])
    for i, b in enumerate(batalhas):
        if b["id"] == batalha_atualizada["id"]:
            batalhas[i] = batalha_atualizada
            return True
    return False

def _gerar_novo_id_batalha(gamestate: dict) -> int:
    max_id = 0
    for batalha in gamestate.get("batalhas_ativas", []):
        if batalha["id"] > max_id:
            max_id = batalha["id"]
    return max_id + 1

def criar_nova_batalha(treinador: dict, pokemon_treinador: dict, pokemon_selvagem_modelo: dict, nivel_selvagem: int, area_id: str) -> dict:
    gamestate = get_gamestate()
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
        "pokemon_em_campo_id_captura": pokemon_treinador["id_captura"],
        "oponente": oponente,
        "log_batalha": [f"Um {oponente['nome']} selvagem (Nível {nivel_selvagem}) apareceu!"],
        "area_id": area_id
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

def deletar_batalha(batalha_id: int, gamestate: dict):
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

def curar_pokemons_treinador(treinador_id: int):
    gamestate = get_gamestate()
    treinador_encontrado = None
    for t in gamestate.get("treinadores", []):
        if t["id"] == treinador_id:
            treinador_encontrado = t
            break      
    if not treinador_encontrado:
        return False
    for pokemon in treinador_encontrado.get("equipe", []):
        if pokemon and "hp_max" in pokemon:
            pokemon["hp"] = pokemon["hp_max"]
    for pokemon in treinador_encontrado.get("pc", []):
        if pokemon and "hp_max" in pokemon:
            pokemon["hp"] = pokemon["hp_max"]
            
    save_gamestate(gamestate)
    return True

def get_ginasio_data_by_id(ginasio_id: str):
    """Carrega os dados de um ginásio específico a partir do JSON."""
    try:
        with open(GINASIOS_FILE, "r", encoding="utf-8") as f:
            todos_ginasios = json.load(f)
            return todos_ginasios.get(ginasio_id)
    except FileNotFoundError:
        return None

def criar_batalha_de_ginasio(treinador: dict, ginasio_id: str) -> dict:
    gamestate = get_gamestate()
    info_ginasio = get_ginasio_data_by_id(ginasio_id)
    
    if not info_ginasio:
        return {"error": "Ginásio não encontrado."}
    
    if treinador.get("ginasios_vencidos", 0) >= int(ginasio_id):
        return {"error": "Você já venceu este ginásio!"}
    equipe_lider = []
    for p_modelo in info_ginasio.get("equipe", []):
        pokedex_info = get_pokemon_from_pokedex_by_id(p_modelo["pokedex_id"])
        if not pokedex_info:
            print(f"AVISO: Pokémon com ID {p_modelo['pokedex_id']} do ginásio não encontrado na pokedex.")
            continue
            
        stats = calcular_stats_pokemon(pokedex_info, p_modelo["nivel"])
        equipe_lider.append({
            "nome": pokedex_info["nome"],
            "nivel": p_modelo["nivel"],
            "hp_max": stats["hp"],
            "hp_atual": stats["hp"],
            "ataque": stats["ataque"],
            "pokedex_id": pokedex_info["id"],
            "tipagem": pokedex_info.get("tipagem", [])
        })
    if not equipe_lider:
        return {"error": f"Falha ao configurar o ginásio. A equipe do líder {info_ginasio.get('lider_nome')} está vazia. Verifique a Pokedex."}
    pokemon_jogador = next((p for p in treinador.get("equipe", []) if p and p.get("hp", 0) > 0), None)
    if not pokemon_jogador:
        return {"error": "Todos os seus Pokémon estão desmaiados!"}

    nova_batalha = {
        "id": _gerar_novo_id_batalha(gamestate),
        "tipo": "GINASIO",
        "treinador_id": treinador["id"],
        "ginasio_id": ginasio_id,
        "pokemon_em_campo_id_captura": pokemon_jogador["id_captura"],
        "oponente_lider": {
            "nome": info_ginasio["lider_nome"],
            "equipe": equipe_lider,
            "pokemon_ativo_idx": 0
        },
        "log_batalha": [f"Você desafiou o Líder de Ginásio {info_ginasio['lider_nome']}!", f"{info_ginasio['lider_nome']} enviou {equipe_lider[0]['nome']}!"]
    }
    
    gamestate.setdefault("batalhas_ativas", []).append(nova_batalha)
    save_gamestate(gamestate)
    return nova_batalha

def processar_acao_batalha_ginasio(batalha_id: int, acao: schemas.AcaoBatalha) -> dict:
    gamestate = get_gamestate()
    batalha = next((b for b in gamestate.get("batalhas_ativas", []) if b["id"] == batalha_id and b.get("tipo") == "GINASIO"), None)
    
    if not batalha:
        return {"error": "Batalha de ginásio não encontrada ou já terminada."}
    treinador_id = batalha["treinador_id"]
    treinador = next((t for t in gamestate.get("treinadores", []) if t["id"] == treinador_id), None)
    if not treinador:
        return {"error": "O treinador para esta batalha não foi encontrado no gamestate."}
    pokemon_jogador = get_pokemon_da_equipe_by_id(treinador["id"], batalha["pokemon_em_campo_id_captura"])
    
    oponente_lider = batalha["oponente_lider"]
    pokemon_ativo_idx = oponente_lider["pokemon_ativo_idx"]
    pokemon_oponente_ativo = oponente_lider["equipe"][pokemon_ativo_idx]
    log = batalha["log_batalha"]

    if acao.tipo == "atacar":
        info_jogador = get_pokemon_from_pokedex_by_id(pokemon_jogador["pokedex_id"])
        info_oponente = get_pokemon_from_pokedex_by_id(pokemon_oponente_ativo["pokedex_id"])
        dano_jogador = int(max(1, (pokemon_jogador["ataque"] / 4)) * type_logic.calcular_multiplicador(info_jogador['tipagem'][0], info_oponente['tipagem']))
        pokemon_oponente_ativo["hp_atual"] -= dano_jogador
        log.append(f"{pokemon_jogador['nome']} usou um ataque e causou {dano_jogador} de dano!")
        if pokemon_oponente_ativo["hp_atual"] > 0:
            dano_oponente = int(max(1, (pokemon_oponente_ativo["ataque"] / 4)) * type_logic.calcular_multiplicador(info_oponente['tipagem'][0], info_jogador['tipagem']))
            pokemon_jogador["hp"] -= dano_oponente
            log.append(f"{pokemon_oponente_ativo['nome']} contra-ataca e causa {dano_oponente} de dano!")

        # --- VERIFICAÇÕES DE FIM DE TURNO ---

        # 1. VERIFICA DERROTA DO JOGADOR (MAIOR PRIORIDADE)
        if pokemon_jogador["hp"] <= 0:
            pokemon_jogador["hp"] = 0
            log.append(f"Seu {pokemon_jogador['nome']} desmaiou!")
            outros_pokemons_aptos = any(p and p["hp"] > 0 for p in treinador.get("equipe", []))
            if not outros_pokemons_aptos:
                log.append(f"Todos os seus Pokémon foram derrotados. Você perdeu a batalha!")
                batalha["resultado_final"] = "Você foi derrotado, corra para o Centro Pokémon!"
                batalha["vitoria"] = False
                deletar_batalha(batalha_id, gamestate)
                save_gamestate(gamestate)
                return batalha

        # 2. VERIFICA DERROTA DO OPONENTE (SE O JOGADOR AINDA ESTIVER EM PÉ)
        if pokemon_oponente_ativo["hp_atual"] <= 0:
            pokemon_oponente_ativo["hp_atual"] = 0
            log.append(f"O {pokemon_oponente_ativo['nome']} do Líder {oponente_lider['nome']} foi derrotado!")
            proximo_pokemon_idx = pokemon_ativo_idx + 1
            if proximo_pokemon_idx < len(oponente_lider["equipe"]):
                oponente_lider["pokemon_ativo_idx"] = proximo_pokemon_idx
                proximo_pokemon = oponente_lider["equipe"][proximo_pokemon_idx]
                log.append(f"{oponente_lider['nome']} enviou {proximo_pokemon['nome']}!")
            else:
                log.append(f"Você derrotou o Líder de Ginásio {oponente_lider['nome']}!")
                batalha["resultado_final"] = f"Parabéns! Você venceu e ganhou a insígnia!"
                batalha["vitoria"] = True
                treinador["ginasios_vencidos"] = max(treinador.get("ginasios_vencidos", 0), int(batalha["ginasio_id"]))
                dar_xp_e_evoluir_equipe(batalha, pokemon_oponente_ativo, gamestate)
                deletar_batalha(batalha_id, gamestate)
                save_gamestate(gamestate)
                return batalha

        atualizar_batalha(batalha, gamestate)
        atualizar_pokemon_na_equipe(treinador["id"], pokemon_jogador, gamestate)
        save_gamestate(gamestate)
        return batalha
        
    elif acao.tipo == "fugir":
        log.append("Você fugiu da batalha de ginásio!")
        batalha["resultado_final"] = "Você fugiu e foi considerado derrotado. Tente novamente!"
        batalha["vitoria"] = False
        deletar_batalha(batalha_id, gamestate)
        save_gamestate(gamestate)
        return batalha
    
    return {"error": "Ação inválida para batalha de ginásio."}