from fastapi import APIRouter, HTTPException
from .. import schemas, crud, type_logic
import random
import math
import traceback

router = APIRouter(
    prefix="/batalha",
    tags=["Batalhas"]
)

@router.post("/iniciar")
def iniciar_batalha(info: schemas.BatalhaInfo):
    treinador = crud.get_treinador_by_id(info.treinador_id)
    pokemon_modelo = crud.get_pokemon_from_pokedex_by_nome(info.pokemon_nome)
    
    if not treinador or not pokemon_modelo:
        raise HTTPException(status_code=404, detail="Treinador ou Pokémon modelo não encontrado.")
    
    equipe_do_treinador = [p for p in treinador.get("equipe", []) if p is not None]
    if not equipe_do_treinador:
        raise HTTPException(status_code=400, detail="Você não tem Pokémon na sua equipe para batalhar!")

    pokemon_apto_para_batalha = next((p for p in equipe_do_treinador if p.get("hp", 0) > 0), None)
    if not pokemon_apto_para_batalha:
        raise HTTPException(status_code=400, detail="Todos os seus Pokémon estão desmaiados! Visite um Centro Pokémon.")

    nova_batalha = crud.criar_nova_batalha(treinador, pokemon_apto_para_batalha, pokemon_modelo, info.nivel_encontrado, info.area_id)
    return nova_batalha

@router.post("/{batalha_id}/acao")
def executar_acao_batalha(batalha_id: int, acao: schemas.AcaoBatalha):
    try:  # DEBUGGER
        gamestate = crud.get_gamestate()
        batalha = next((b for b in gamestate.get("batalhas_ativas", []) if b["id"] == batalha_id), None)
        
        if not batalha:
            raise HTTPException(status_code=404, detail="A batalha já terminou ou não foi encontrada.")

        treinador = next((t for t in gamestate.get("treinadores", []) if t["id"] == batalha["treinador_id"]), None)
        if not treinador:
            raise HTTPException(status_code=404, detail="Treinador da batalha não foi encontrado.")

        pokemon_em_campo = crud.get_pokemon_da_equipe_by_id(treinador['id'], batalha["pokemon_em_campo_id_captura"])
        if not pokemon_em_campo:
            crud.deletar_batalha(batalha_id, gamestate)
            crud.save_gamestate(gamestate)
            raise HTTPException(status_code=500, detail="Erro fatal: Pokémon em campo não existe mais. Batalha encerrada.")

        oponente = batalha["oponente"]
        log = batalha["log_batalha"]

        # AÇÃO: FUGIR
        if acao.tipo == "fugir":
            crud.deletar_batalha(batalha_id, gamestate)
            batalha['resultado_final'] = "Você fugiu com sucesso!"
            crud.save_gamestate(gamestate)
            return batalha

        # AÇÃO: CAPTURAR
        elif acao.tipo == "capturar":
            porcentagem_hp = oponente["hp_atual"] / oponente["hp_max"]
            chance = 0.2
            if porcentagem_hp <= 0.25: chance = 0.5
            elif porcentagem_hp <= 0.50: chance = 0.4
            elif porcentagem_hp <= 0.75: chance = 0.3
            
            log.append("Você tenta capturar...")
            if random.random() < chance:
                log.append(f"{oponente['nome']} foi capturado!")
                stats = crud.calcular_stats_pokemon(crud.get_pokemon_from_pokedex_by_id(oponente['pokedex_id']), oponente['nivel'])
                novo_pokemon = {"id_captura": crud.gerar_novo_id_captura(), "pokedex_id": oponente['pokedex_id'], "nome": oponente['nome'], "nivel": oponente['nivel'], "hp_max": stats['hp'],"hp": oponente['hp_atual'], "ataque": stats['ataque'], "xp_atual": 0, "xp_para_upar": crud.calcular_xp_necessario(oponente['nivel'] + 1)}
                crud.adicionar_pokemon_ao_treinador(treinador['id'], novo_pokemon, gamestate)
                crud.deletar_batalha(batalha_id, gamestate) 
                batalha['resultado_final'] = f"{oponente['nome']} foi capturado!"
                crud.save_gamestate(gamestate)
                return batalha
            else:
                log.append("A captura falhou!")
                dano_oponente = max(1, math.floor(oponente["ataque"] / 4) + random.randint(-2, 2))
                pokemon_em_campo["hp"] -= dano_oponente
                log.append(f"{oponente['nome']} contra-ataca e causa {dano_oponente} de dano!")
                if pokemon_em_campo["hp"] <= 0:
                    pokemon_em_campo["hp"] = 0
                    log.append("Seu Pokémon desmaiou!")
                    crud.deletar_batalha(batalha_id, gamestate)
                    batalha['resultado_final'] = "Você foi derrotado..."
                crud.atualizar_pokemon_na_equipe(treinador['id'], pokemon_em_campo, gamestate)
                crud.save_gamestate(gamestate)
                return batalha

        # AÇÃO: ATACAR
        elif acao.tipo == "atacar":
            atacante_info = crud.get_pokemon_from_pokedex_by_id(pokemon_em_campo['pokedex_id'])
            defensor_info = crud.get_pokemon_from_pokedex_by_id(oponente['pokedex_id'])
            
            dano_jogador = int(max(1, math.floor(pokemon_em_campo["ataque"]/4)) * type_logic.calcular_multiplicador(atacante_info['tipagem'][0], defensor_info['tipagem']))
            oponente["hp_atual"] -= dano_jogador
            log.append(f"{pokemon_em_campo['nome']} ataca e causa {dano_jogador} de dano!")

            if oponente["hp_atual"] <= 0:
                oponente["hp_atual"] = 0
                log.append(f"{oponente['nome']} desmaiou! Você venceu!")
                logs_de_xp = crud.dar_xp_e_evoluir_equipe(batalha, oponente, gamestate)
                log.extend(logs_de_xp)
                crud.deletar_batalha(batalha_id, gamestate)
                batalha['resultado_final'] = "Vitória!"
                crud.save_gamestate(gamestate)
                return batalha
            
            dano_oponente = int(max(1, math.floor(oponente["ataque"]/4)) * type_logic.calcular_multiplicador(defensor_info['tipagem'][0], atacante_info['tipagem']))
            pokemon_em_campo["hp"] -= dano_oponente
            log.append(f"{oponente['nome']} contra-ataca e causa {dano_oponente} de dano!")

            if pokemon_em_campo["hp"] <= 0:
                pokemon_em_campo["hp"] = 0
                log.append(f"Seu {pokemon_em_campo['nome']} desmaiou!")
                outros_pokemons_aptos = any(p and p.get("hp", 0) > 0 for p in treinador.get("equipe", []))
                crud.deletar_batalha(batalha_id, gamestate)
                batalha['resultado_final'] = "Você foi derrotado..."

            crud.atualizar_batalha(batalha, gamestate)
            crud.atualizar_pokemon_na_equipe(treinador['id'], pokemon_em_campo, gamestate)
            crud.save_gamestate(gamestate)
            return batalha
        
        raise HTTPException(status_code=400, detail="Ação inválida.")
    
    except Exception as e:
        print("\n\n!!!!!! ERRO GRAVE NO BACKEND !!!!!!\n")
        traceback.print_exc()
        print("\n!!!!!! FIM DO ERRO GRAVE !!!!!!\n\n")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{batalha_id}/trocar")
def trocar_pokemon_em_batalha(batalha_id: int, acao: schemas.AcaoTroca):
    gamestate = crud.get_gamestate()
    batalha = crud.get_batalha_by_id(batalha_id)
    if not batalha:
        raise HTTPException(status_code=404, detail="Batalha não encontrada.")
        
    treinador = crud.get_treinador_by_id(batalha["treinador_id"])
    pokemon_para_trocar = crud.get_pokemon_da_equipe_by_id(treinador["id"], acao.id_captura_para_troca)
    pokemon_em_campo_antigo = crud.get_pokemon_da_equipe_by_id(treinador["id"], batalha["pokemon_em_campo_id_captura"])
    if not pokemon_para_trocar:
        raise HTTPException(status_code=404, detail="Pokémon escolhido para troca não foi encontrado na sua equipe.")
    if pokemon_para_trocar["hp"] <= 0:
        raise HTTPException(status_code=400, detail="Você não pode trocar para um Pokémon desmaiado!")
    if pokemon_para_trocar["id_captura"] == batalha["pokemon_em_campo_id_captura"]:
        raise HTTPException(status_code=400, detail="Este Pokémon já está em batalha!")

    batalha["pokemon_em_campo_id_captura"] = acao.id_captura_para_troca
    batalha["log_batalha"].append(f"{pokemon_em_campo_antigo['nome']}, volte! Vai, {pokemon_para_trocar['nome']}!")
    
    oponente = batalha["oponente"]
    atacante_info_oponente = crud.get_pokemon_from_pokedex_by_id(oponente['pokedex_id'])
    defensor_info = crud.get_pokemon_from_pokedex_by_id(pokemon_para_trocar['pokedex_id'])
    
    dano_oponente = int(max(1, math.floor(oponente["ataque"]/4)) * type_logic.calcular_multiplicador(atacante_info_oponente['tipagem'][0], defensor_info['tipagem']))
    pokemon_para_trocar["hp"] -= dano_oponente
    batalha["log_batalha"].append(f"{oponente['nome']} ataca e causa {dano_oponente} de dano!")
    
    if pokemon_para_trocar["hp"] <= 0:
        pokemon_para_trocar["hp"] = 0
        batalha["log_batalha"].append(f"Seu {pokemon_para_trocar['nome']} desmaiou!")
        crud.deletar_batalha(batalha_id, gamestate)
        batalha['resultado_final'] = "Você foi derrotado..."

    # Salva as alterações
    crud.atualizar_pokemon_na_equipe(treinador['id'], pokemon_para_trocar, gamestate)
    crud.atualizar_batalha(batalha, gamestate)
    crud.save_gamestate(gamestate)

    return batalha