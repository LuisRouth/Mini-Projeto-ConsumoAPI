import sys
import os
import tkinter as tk
from tkinter import messagebox
import threading
import uvicorn
import requests
import time


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa as telas
from ui.tela_login import TelaLogin
from ui.tela_escolha import TelaEscolha
from ui.tela_geral import TelaGeral
from ui.tela_encontro import TelaEncontro
from ui.tela_batalha import TelaBatalha

# --- MÓDULO API E VARIÁVEIS GLOBAIS ---
API_URL = "http://127.0.0.1:8000"
treinador_atual = None
batalha_atual = None

class ApiClient:
    def _request(self, method, endpoint, json_data=None):
        try:
            response = requests.request(method, f"{API_URL}{endpoint}", json=json_data)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"ERRO CRÍTICO DE API: {e}")
            messagebox.showerror("Erro Crítico de API", f"Não foi possível conectar ao servidor em {API_URL}.\nVerifique se o backend está rodando.\n\n{e}")
            sys.exit(1)
            
    def criar_treinador(self, nome):
        return self._request('post', '/treinador', {'nome': nome})

    def buscar_iniciais(self):
        return self._request('get', '/pokedex/iniciais')
    
    def escolher_inicial(self, treinador_id, pokemon_nome):
        return self._request('post', f'/treinador/{treinador_id}/escolher-inicial', {'pokemon_nome': pokemon_nome})
    
    def encontrar_pokemon(self):
        return self._request('get', '/mundo/encontrar-pokemon')

    def iniciar_batalha(self, treinador_id, pokemon_nome):
        return self._request('post', '/batalha/iniciar', {'treinador_id': treinador_id, 'pokemon_nome': pokemon_nome})
    
    def executar_acao_batalha(self, batalha_id, tipo_acao):
        return self._request('post', f'/batalha/{batalha_id}/acao', {'tipo': tipo_acao})

    def get_batalha(self, batalha_id):
        return self._request('get', f'/batalha/{batalha_id}')

    def get_pc(self, treinador_id):
        return self._request('get', f'/treinador/{treinador_id}/pc')

api = ApiClient()

# --- CLASSE CONTROLADORA PRINCIPAL ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cliente Pokémon")
        self.attributes('-fullscreen', True)
        self.bind('<Escape>', self.fechar_tela_cheia)
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.mostrar_frame(TelaLogin)

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
            iniciais = api.buscar_iniciais()
            if iniciais:
                self.mostrar_frame(TelaEscolha, iniciais)

    def handle_escolher_inicial(self, pokemon_nome):
        global treinador_atual
        pokemon_escolhido = api.escolher_inicial(treinador_atual['id'], pokemon_nome)
        
        if pokemon_escolhido:
             messagebox.showinfo("Sucesso", f"Você e {pokemon_nome} começam uma nova jornada!")
             self.mostrar_frame(TelaGeral)
    
    def get_treinador_pc(self):
        return treinador_atual['pc'] if treinador_atual else []

    def handle_procurar_pokemon(self):
        pokemon_encontrado = api.encontrar_pokemon()
        if pokemon_encontrado:
            if hasattr(self.current_frame, 'mostrar_encontro'):
                self.current_frame.mostrar_encontro(pokemon_encontrado)

    def handle_iniciar_batalha(self, pokemon_nome):
        global batalha_atual, treinador_atual
        batalha_atual = api.iniciar_batalha(treinador_atual['id'], pokemon_nome)
        if batalha_atual:
            # Traz o pc atualizado para o estado global
            treinador_atual['pc'] = api.get_pc(treinador_atual['id'])
            self.mostrar_frame(TelaBatalha, batalha_atual)

    def handle_acao_batalha(self, batalha_id, tipo_acao):
        global batalha_atual
        resultado = api.executar_acao_batalha(batalha_id, tipo_acao)
        
        if resultado:
            if tipo_acao == 'fugir' or "Vitória" in resultado['resultado'] or "derrotado" in resultado['resultado']:
                messagebox.showinfo("Batalha Encerrada", resultado['resultado'])
                self.mostrar_frame(TelaGeral) # Volta para a tela geral
            else:
                # Se a batalha continua, busca o estado atualizado e redesenha a tela
                batalha_atual = api.get_batalha(batalha_id)
                # Pega o PC atualizado para refletir o dano
                treinador_atual['pc'] = api.get_pc(treinador_atual['id']) 
                if batalha_atual and hasattr(self.current_frame, 'atualizar_interface'):
                    self.current_frame.atualizar_interface(batalha_atual)

    def mostrar_aviso(self, mensagem):
        messagebox.showwarning("Aviso", mensagem)

# --- INICIALIZAÇÃO DA APLICAÇÃO ---
def start_backend():
    try:
        requests.get(f"{API_URL}/", timeout=1)
        print("--- [BACKEND] Servidor já estava no ar. ---")
    except requests.exceptions.ConnectionError:
        print("--- [BACKEND] Iniciando Servidor da API na porta 8000... ---")
        uvicorn.run("server.app.main:app", host="127.0.0.1", port=8000, log_level="warning")

if __name__ == "__main__":
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    print("--- [FRONTEND] Esperando o backend ficar pronto... ---")
    time.sleep(2) 

    app = App()
    app.mainloop()