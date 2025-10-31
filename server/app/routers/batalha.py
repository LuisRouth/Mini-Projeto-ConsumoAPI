from fastapi import APIRouter, HTTPException
from .. import schemas, crud
import random
import math

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
    if not treinador.get("pc"):
        raise HTTPException(status_code=400, detail="Treinador sem Pokémon para batalhar.")
    pokemon_do_treinador = treinador["pc"][0]

    nova_batalha = crud.criar_nova_batalha(treinador, pokemon_do_treinador, pokemon_modelo)
    
    return nova_batalha

@router.get("/{batalha_id}")
def get_batalha_ativa(batalha_id: int):
    batalha = crud.get_batalha_by_id(batalha_id)
    if not batalha:
        raise HTTPException(status_code=404, detail="Batalha não encontrada.")
    return batalha

@router.post("/{batalha_id}/acao")
def executar_acao_batalha(batalha_id: int, acao: schemas.AcaoBatalha):
    batalha = crud.get_batalha_by_id(batalha_id)
    if not batalha:
        raise HTTPException(status_code=404, detail="A batalha já terminou.")

    pokemon_em_campo = crud.get_pokemon_do_pc_by_id(batalha["treinador_id"], batalha["pokemon_em_campo_id_captura"])
    oponente = batalha["oponente"]
    log = batalha["log_batalha"]

    # --- LÓGICA DAS AÇÕES ---
    if acao.tipo == "fugir":
        crud.deletar_batalha(batalha_id)
        return {"resultado": "Você fugiu com sucesso!"}

    if acao.tipo == "capturar":
        porcentagem_hp = oponente["hp_atual"] / oponente["hp_max"]
        chance_base = 0.5
        chance_captura = (1 - porcentagem_hp) * chance_base

        if random.random() < chance_captura:
            log.append(f"Parabéns! {oponente['nome']} foi capturado!")
            
            # --- LÓGICA DE CAPTURA ---
            pokemon_modelo_capturado = crud.get_pokemon_from_pokedex_by_id(oponente['pokedex_id'])
            
            novo_pokemon_capturado = {
                "id_captura": crud.gerar_novo_id_captura(),
                "pokedex_id": pokemon_modelo_capturado["id"],
                "nome": pokemon_modelo_capturado["nome"],
                "nivel": oponente['nivel'],
                "hp": oponente['hp_atual'],
                "ataque": oponente['ataque']
            }
            # ------------------------------------

            crud.adicionar_pokemon_ao_pc(batalha['treinador_id'], novo_pokemon_capturado)
            crud.deletar_batalha(batalha_id)
            return {"resultado": f"{oponente['nome']} foi capturado com sucesso!"}
        else:
            log.append("A captura falhou!")
            dano_oponente = max(1, math.floor(oponente["ataque"] / 4) + random.randint(-2, 2))
            pokemon_em_campo["hp"] -= dano_oponente
            log.append(f"{oponente['nome']} atacou e causou {dano_oponente} de dano!")
            crud.atualizar_pokemon_no_pc(batalha['treinador_id'], pokemon_em_campo)

    elif acao.tipo == "atacar":
        dano_base_jogador = math.floor(pokemon_em_campo["ataque"] / 4) + random.randint(-3, 3)
        dano_jogador = max(1, dano_base_jogador)
        oponente["hp_atual"] -= dano_jogador
        log.append(f"{pokemon_em_campo['nome']} ataca e causa {dano_jogador} de dano!")

        if oponente["hp_atual"] <= 0:
            oponente["hp_atual"] = 0
            log.append(f"O {oponente['nome']} selvagem desmaiou! Você venceu a batalha!")
            crud.deletar_batalha(batalha_id)
            crud.atualizar_pokemon_no_pc(batalha['treinador_id'], pokemon_em_campo) # Salva o HP alterado do seu pokémon
            return {"resultado": "Vitória!"}
        
        dano_base_oponente = math.floor(oponente["ataque"] / 4) + random.randint(-3, 3)
        dano_oponente = max(1, dano_base_oponente)
        pokemon_em_campo["hp"] -= dano_oponente
        log.append(f"O {oponente['nome']} contra-ataca e causa {dano_oponente} de dano!")
        
        if pokemon_em_campo["hp"] <= 0:
            pokemon_em_campo["hp"] = 0
            log.append(f"Seu {pokemon_em_campo['nome']} desmaiou! Você foi derrotado!")
            crud.save_gamestate(crud.get_gamestate())

            if pokemon_em_campo['hp'] <= 0:
                crud.deletar_batalha(batalha_id)
                return {"resultado": "Você foi derrotado..."}
            if oponente['hp_atual'] <= 0:
                crud.deletar_batalha(batalha_id)
                return {"resultado": "Vitória!"}

            return {"resultado": "Turno concluído."}
