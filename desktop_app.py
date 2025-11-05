import sys
import os
import customtkinter as ctk  # Use CustomTkinter, não Tkinter
from ui.popup_padrao import PopupPadrao  # Novo padrão!
import threading
import uvicorn
import requests
import time
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa as telas adaptadas CustomTkinter
from ui.tela_login import TelaLogin
from ui.tela_escolha import TelaEscolha
from ui.tela_geral import TelaGeral
from ui.tela_encontro import TelaEncontro
from ui.tela_batalha import TelaBatalha
from ui.tela_pc import TelaPC

API_URL = "http://127.0.0.1:8000"
treinador_atual = None
batalha_atual = None

class ApiClient:
    def _request(self, method, endpoint, json_data=None):
        try:
            response = requests.request(method, f"{API_URL}{endpoint}", json=json_data)
            response.raise_for_status()
            # Respostas DELETE podem não ter corpo JSON
            if response.status_code == 204: # 204 No Content
                return {"detail": "Operação bem-sucedida"}
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"ERRO DE HTTP: {http_err} - URL: {http_err.request.url}")
            raise http_err
        except requests.exceptions.RequestException as e:
            print(f"ERRO CRÍTICO DE CONEXÃO: {e}")
            # Padrão CustomTkinter/PopupPadrao em vez de messagebox
            PopupPadrao(None, f"Não foi possível conectar ao servidor.\n{e}", titulo="Erro Crítico de Conexão", tipo="erro")
            sys.exit(1)
           
    def get_pokedex(self):
        return self._request('get', '/pokedex')

    def criar_treinador(self, nome):
        return self._request('post', '/treinador', {'nome': nome})
    
    def get_treinador(self, treinador_id):
        return self._request('get', f'/treinador/{treinador_id}')

    def buscar_iniciais(self):
        return self._request('get', '/pokedex/iniciais')
    
    def escolher_inicial(self, treinador_id, pokemon_nome):
        return self._request('post', f'/treinador/{treinador_id}/escolher-inicial', {'pokemon_nome': pokemon_nome})
    
    def get_pokedex_info(self, pokedex_id):
        for pokemon in self.pokedex_data:
            if pokemon['id'] == pokedex_id:
                return pokemon
        return None
    
    def desafiar_ginasio(self, ginasio_id, treinador_id):
        return self._request('post', f'/ginasio/{ginasio_id}/desafiar', json_data={'treinador_id': treinador_id})
    
    def trocar_pokemon_batalha_ginasio(self, batalha_id, id_captura):
        payload = {'id_captura_para_troca': id_captura}
        return self._request('post', f'/ginasio/batalha/{batalha_id}/trocar', payload)

    def executar_acao_batalha_ginasio(self, batalha_id, tipo_acao):
        return self._request('post', f'/ginasio/batalha/{batalha_id}/acao', {'tipo': tipo_acao})
    
    def get_areas(self):
        return self._request('get', '/mundo/areas')
    
    def encontrar_pokemon(self, area_id: str):
        return self._request('get', f'/mundo/encontrar-pokemon?area_id={area_id}')

    def iniciar_batalha(self, treinador_id, pokemon_nome, nivel, area_id):
        payload = {
            'treinador_id': treinador_id,
            'pokemon_nome': pokemon_nome,
            'nivel_encontrado': nivel,
            'area_id': area_id
        }
        return self._request('post', '/batalha/iniciar', payload)
    
    def executar_acao_batalha(self, batalha_id, tipo_acao):
        return self._request('post', f'/batalha/{batalha_id}/acao', {'tipo': tipo_acao})

    def get_batalha(self, batalha_id):
        return self._request('get', f'/batalha/{batalha_id}')
    
    def trocar_pokemon(self, batalha_id, id_captura):
        payload = {'id_captura_para_troca': id_captura}
        return self._request('post', f'/batalha/{batalha_id}/trocar', payload)
    
    def get_equipe(self, treinador_id):
        return self._request('get', f'/treinador/{treinador_id}/equipe')
        
    def treinar_pokemon(self, treinador_id, id_captura, area_id):
        return self._request('post', f'/treinador/{treinador_id}/treinar/{id_captura}?area_atual={area_id}')

    def get_pc(self, treinador_id):
        return self._request('get', f'/treinador/{treinador_id}/pc')
    
    def trocar_posicao(self, treinador_id, id1, id2, lista):
        url = f"/treinador/{treinador_id}/trocar-posicao?id1={id1}&id2={id2}&lista={lista}"
        return self._request('post', url)
    
    def organizar_pc(self, treinador_id, id_captura, origem):
        url = f"/treinador/{treinador_id}/organizar-pc?id_captura={id_captura}&origem={origem}"
        return self._request('post', url)
    
    def mover_pokemon(self, treinador_id, id_captura, de_lista, de_index, para_lista, para_index):
            url = (
                f"/treinador/{treinador_id}/mover-pokemon"
                f"?id_captura={id_captura}"
                f"&de_lista={de_lista}&de_index={de_index}"
                f"&para_lista={para_lista}&para_index={para_index}"
            )
            return self._request('post', url)

    def curar_pokemons(self, treinador_id):
        return self._request('post', f'/treinador/{treinador_id}/curar')

    # --- NOVO RECURSO: Adicionado endpoint de exclusão ---
    def delete_pokemon(self, treinador_id, id_captura):
        # O backend DEVE implementar este endpoint:
        # Ex: DELETE /treinador/1/pokemon/5
        return self._request('delete', f'/treinador/{treinador_id}/pokemon/{id_captura}')

api = ApiClient()

# --- CLASSE CONTROLADORA PRINCIPAL ---

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cliente Pokémon")
        self.attributes('-fullscreen', True)
        self.bind('<Escape>', self.fechar_tela_cheia)

        self.container = ctk.CTkFrame(self)
        self.pokedex_data = api.get_pokedex()
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.pokemon_selecionado_pc = None
        self.origem_selecao_pc = None
        self.troca_window = None
        self.batalha_atual = None
        self.pc_window = None # Garantir que pc_window está definido

        self.mostrar_frame(TelaLogin)

    def mostrar_aviso_padrao(self, mensagem, tipo="info", titulo="Aviso"):
        PopupPadrao(self, mensagem, titulo, tipo)

    def fechar_tela_cheia(self, event=None):
        self.attributes('-fullscreen', False)

    def mostrar_frame(self, Page, args=None):
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        if args:
            self.current_frame = Page(self.container, self, args)
        else:
            self.current_frame = Page(self.container, self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def get_treinador_nome(self):
        return treinador_atual['nome'] if treinador_atual else "Convidado"

    def handle_criar_treinador(self, nome):
        global treinador_atual
        treinador_atual = api.criar_treinador(nome)
        if treinador_atual:
            self.pokedex_data = api.get_pokedex()
            iniciais = api.buscar_iniciais()
            if iniciais:
                self.mostrar_frame(TelaEscolha, iniciais)

    def handle_abrir_pc(self):
        self.pokemon_selecionado_pc = None
        self.origem_selecao_pc = None
        self.pc_window = TelaPC(self, self)

    def get_pokedex_info(self, pokedex_id):
        for pokemon in self.pokedex_data:
            if pokemon.get('id') == pokedex_id:
                return pokemon
        return None

    def handle_escolher_inicial(self, pokemon_nome):
        global treinador_atual
        try:
            pokemon_escolhido = api.escolher_inicial(treinador_atual['id'], pokemon_nome)
            if pokemon_escolhido:
                self.mostrar_aviso_padrao(f"Você e {pokemon_nome} começam uma nova jornada!", tipo="sucesso", titulo="Sucesso")
                self.mostrar_frame(TelaGeral)
        except requests.exceptions.HTTPError as e:
            erro_msg = e.response.json().get("detail", "Erro ao escolher o Pokémon.")
            self.mostrar_aviso_padrao(erro_msg, tipo="erro", titulo="Erro")

    def handle_desafiar_ginasio(self, ginasio_id: str):
        global treinador_atual, batalha_atual
        try:
            resposta_batalha = api.desafiar_ginasio(ginasio_id, treinador_atual['id'])
            if resposta_batalha:
                batalha_atual = resposta_batalha
                from ui.tela_batalha_ginasio import TelaBatalhaGinasio
                self.mostrar_frame(TelaBatalhaGinasio, batalha_atual)
        except requests.exceptions.HTTPError as e:
            erro_msg = e.response.json().get("detail", "Não foi possível iniciar o desafio.")
            self.mostrar_aviso_padrao(erro_msg, tipo="erro", titulo="Erro de Desafio")

    def handle_acao_batalha_ginasio(self, batalha_id, tipo_acao):
        global batalha_atual, treinador_atual
        try:
            resposta_batalha = api.executar_acao_batalha_ginasio(batalha_id, tipo_acao)
            batalha_atual = resposta_batalha
            if hasattr(self.current_frame, 'atualizar_interface'):
                self.current_frame.atualizar_interface(batalha_atual)
            if 'resultado_final' in batalha_atual:
                self.mostrar_aviso_padrao(batalha_atual['resultado_final'], tipo="info", titulo="Batalha de Ginásio Terminada")
                treinador_atual = api.get_treinador(treinador_atual['id'])
                self.mostrar_frame(TelaGeral)
                return
            if batalha_atual.get("estado") == "AGUARDANDO_TROCA":
                self.handle_mostrar_tela_troca(is_forced=True)
        except requests.exceptions.HTTPError as e:
            erro_msg = e.response.json().get("detail", "Ocorreu um erro na batalha.")
            self.mostrar_aviso_padrao(erro_msg, tipo="erro", titulo="Erro de Batalha")

    def handle_pc_click(self, clique_info):
        global treinador_atual
        lista_clicada, index_clicado, pokemon_clicado = clique_info
        pc_win = self.pc_window
        if not self.pokemon_selecionado_pc:
            if not pokemon_clicado: return
            self.pokemon_selecionado_pc = pokemon_clicado
            self.origem_selecao_pc = (lista_clicada, index_clicado)
            if pc_win and pc_win.winfo_exists():
                pc_win.feedback_label.configure(text=f"Selecionado: {pokemon_clicado['nome']}")
        else:
            pokemon_na_mao = self.pokemon_selecionado_pc
            de_lista, de_index = self.origem_selecao_pc
            try:
                resultado = api.mover_pokemon(
                    treinador_atual['id'], pokemon_na_mao['id_captura'],
                    de_lista, de_index, lista_clicada, index_clicado
                )
                print(resultado.get('mensagem', 'Movimento realizado.'))
            except requests.exceptions.HTTPError as e:
                erro_msg = e.response.json().get("detail", "Erro desconhecido.")
                self.mostrar_aviso_padrao(erro_msg, tipo="erro", titulo="Movimento Inválido")
            finally:
                self.pokemon_selecionado_pc = None
                self.origem_selecao_pc = None
                if pc_win and pc_win.winfo_exists():
                    pc_win.redesenhar_widgets()
                    pc_win.feedback_label.configure(text="Pokémon movido! Selecione o próximo.")

    # --- NOVO RECURSO: Handler para exclusão ---
    def handle_excluir_pokemon(self, id_captura, nome_pokemon):
        global treinador_atual
        pc_win = self.pc_window
        
        # AQUI VOCÊ PODE ADICIONAR UM POPUP DE CONFIRMAÇÃO SE QUISER
        # print(f"Tentando excluir {nome_pokemon} (ID: {id_captura})")
        
        try:
            # Chamar a nova função da API
            resultado = api.delete_pokemon(treinador_atual['id'], id_captura)
            self.mostrar_aviso_padrao(f"{nome_pokemon} foi libertado com sucesso.", tipo="sucesso", titulo="Pokémon Libertado")
        except requests.exceptions.HTTPError as e:
            # Tenta pegar a mensagem de erro da API
            try:
                erro_msg = e.response.json().get("detail", "Erro desconhecido ao excluir.")
            except:
                erro_msg = "Erro desconhecido ao excluir."
            self.mostrar_aviso_padrao(erro_msg, tipo="erro", titulo="Erro")
        except Exception as e:
            # Lidar com o fato de que o endpoint pode não existir
            print(f"Erro ao excluir: {e}")
            self.mostrar_aviso_padrao(f"Erro ao excluir: {e}\n(Endpoint de exclusão já implementado no servidor?)", tipo="erro")
        finally:
            # Redesenhar a tela do PC
            if pc_win and pc_win.winfo_exists():
                pc_win.redesenhar_widgets()


    def handle_procurar_pokemon(self, area_id: str):
        pokemon_encontrado = api.encontrar_pokemon(area_id)
        if pokemon_encontrado:
            if hasattr(self.current_frame, 'mostrar_encontro'):
                self.current_frame.mostrar_encontro(pokemon_encontrado)

    def handle_iniciar_batalha(self, pokemon_encontrado):
        global batalha_atual, treinador_atual
        try:
            area_atual_id = self.current_frame.area_selecionada_id
            resposta_batalha = api.iniciar_batalha(
                treinador_atual['id'],
                pokemon_encontrado['nome'],
                pokemon_encontrado['nivel'],
                area_atual_id
            )
            if resposta_batalha:
                batalha_atual = resposta_batalha
                self.batalha_atual = resposta_batalha
                treinador_atual['pc'] = api.get_pc(treinador_atual['id'])
                self.mostrar_frame(TelaBatalha, self.batalha_atual)
        except requests.exceptions.HTTPError as e:
            erro_msg = e.response.json().get("detail", "Não foi possível iniciar a batalha.")
            self.mostrar_aviso_padrao(erro_msg, tipo="erro", titulo="Erro")

    def handle_mostrar_tela_troca(self, is_forced: bool = False):
        global treinador_atual
        equipe_disponivel = [p for p in self.get_treinador_equipe() if p and p.get('hp', 0) > 0]
        if not equipe_disponivel:
            self.mostrar_aviso_padrao("Você não tem mais Pokémon para lutar. A batalha terminou!", tipo="info", titulo="Batalha Perdida")
            treinador_atual = api.get_treinador(treinador_atual['id'])
            self.mostrar_frame(TelaGeral)
            return
        from ui.tela_troca_pokemon import TelaTrocaPokemon
        self.troca_window = TelaTrocaPokemon(self, self, is_forced)

    def handle_trocar_pokemon(self, id_captura):
        global batalha_atual, treinador_atual
        if not batalha_atual: return
        try:
            resposta_batalha = None
            if batalha_atual.get('tipo') == 'GINASIO':
                resposta_batalha = api.trocar_pokemon_batalha_ginasio(batalha_atual['id'], id_captura)
            else:
                resposta_batalha = api.trocar_pokemon(batalha_atual['id'], id_captura)
            if resposta_batalha:
                batalha_atual = resposta_batalha
                self.batalha_atual = resposta_batalha
            if self.troca_window and self.troca_window.winfo_exists():
                self.troca_window.destroy()
            if hasattr(self.current_frame, 'atualizar_interface'):
                self.current_frame.atualizar_interface(batalha_atual)
            if 'resultado_final' in batalha_atual:
                self.mostrar_aviso_padrao(batalha_atual['resultado_final'], tipo="info", titulo="Batalha Encerrada")
                treinador_atual = api.get_treinador(treinador_atual['id'])
                self.mostrar_frame(TelaGeral)
                return
        except requests.exceptions.HTTPError as e:
            erro_msg = e.response.json().get("detail", "Não foi possível trocar o Pokémon.")
            self.mostrar_aviso_padrao(erro_msg, tipo="erro", titulo="Erro de Troca")

    def handle_acao_batalha(self, batalha_id, tipo_acao):
        global batalha_atual, treinador_atual
        resposta_batalha = api.executar_acao_batalha(batalha_id, tipo_acao)
        if not resposta_batalha:
            self.mostrar_aviso_padrao("Ocorreu um erro na comunicação com o servidor.", tipo="erro")
            return
        batalha_atual = resposta_batalha
        treinador_atual['pc'] = api.get_pc(treinador_atual['id'])
        if hasattr(self.current_frame, 'atualizar_interface'):
            self.current_frame.atualizar_interface(batalha_atual)
        if 'resultado_final' in batalha_atual:
            self.mostrar_aviso_padrao(batalha_atual['resultado_final'], tipo="info", titulo="Batalha Encerrada")
            self.mostrar_frame(TelaGeral)

    def get_treinador_equipe(self):
        global treinador_atual
        if treinador_atual:
            equipe_atualizada = api.get_equipe(treinador_atual['id'])
            treinador_atual['equipe'] = equipe_atualizada
            return treinador_atual.get('equipe', [])
        return []

    # --- CORREÇÃO DO BUG DE MOVIMENTAÇÃO ---
    def get_treinador_pc(self):
        global treinador_atual
        if treinador_atual:
            # O bug estava aqui. Agora buscamos dados frescos da API.
            pc_atualizado = api.get_pc(treinador_atual['id'])
            treinador_atual['pc'] = pc_atualizado
            return pc_atualizado
        return []
    # --- FIM DA CORREÇÃO ---

    def get_ginasios_vencidos(self):
        global treinador_atual
        if treinador_atual:
            return treinador_atual.get('ginasios_vencidos', [])
        return []

    def handle_fechar_pc(self):
        # Quando fechar o PC, atualiza a TelaGeral
        # para refletir quaisquer mudanças na equipe.
        self.mostrar_frame(TelaGeral)

    def handle_curar_pokemon(self):
        global treinador_atual
        if treinador_atual:
            resultado = api.curar_pokemons(treinador_atual['id'])
            if resultado:
                # Atualiza a equipe na TelaGeral após curar
                if hasattr(self, 'current_frame') and isinstance(self.current_frame, TelaGeral):
                    self.current_frame.desenhar_equipe(self.current_frame.equipe_container)
                self.mostrar_aviso_padrao(resultado['mensagem'], tipo="info", titulo="Centro Pokémon")

    def api_get_areas(self):
        return api.get_areas()


########

# --- INICIALIZAÇÃO DA APLICAÇÃO ---
def start_backend():
    try:
        requests.get(f"{API_URL}/", timeout=1)
        print("--- [BACKEND] Servidor já estava no ar. ---")
    except requests.exceptions.ConnectionError:
        print("--- [BACKEND] Iniciando Servidor da API na porta 8000... ---")
        uvicorn.run("server.app.main:app", host="127.0.0.1", port=8000, log_level="info")

# --- FUNÇÃO PARA RESETAR O JOGO ---
def resetar_gamestate_se_necessario():
    try:
        app_dir = os.path.dirname(os.path.abspath(__file__))
        gamestate_file = os.path.join(app_dir, "server", "app", "gamestate.json")
        estado_limpo = {
            "batalhas_ativas": [],
            "treinadores": []
        }
        with open(gamestate_file, "w", encoding="utf-8") as f:
            json.dump(estado_limpo, f, indent=2)
        print("--- [SISTEMA] gamestate.json foi resetado para um novo jogo. ---")
    except Exception as e:
        # Se quiser avisar visual, use PopupPadrao aqui também, se já estiver com janela criada.
        print(f"--- [ERRO] Não foi possível resetar o gamestate.json: {e} ---")

if __name__ == "__main__":
    resetar_gamestate_se_necessario()
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    print("--- [FRONTEND] Esperando o backend ficar pronto... ---")
    time.sleep(2)
    app = App()
    app.mainloop()

#######