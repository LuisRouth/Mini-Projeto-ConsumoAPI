# ui/tela_batalha_ginasio.py - CÓDIGO CORRIGIDO E COMPLETO

import tkinter as tk

class TelaBatalhaGinasio(tk.Frame):
    def __init__(self, master, controller, batalha_info):
        super().__init__(master)
        self.controller = controller
        self.batalha_id = batalha_info['id']

        # --- ESTRUTURA VISUAL (COPIADA DE TELA_BATALHA.PY) ---
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        status_frame = tk.Frame(self, bd=1, relief="sunken")
        status_frame.grid(row=0, column=0, sticky="nsew")
        
        status_frame.rowconfigure((0, 1), weight=1)
        status_frame.columnconfigure((0, 1), weight=1)

        # Lado do Oponente
        oponente_frame = tk.Frame(status_frame)
        oponente_frame.grid(row=0, column=1, sticky="ne", padx=20, pady=20)
        self.label_oponente_nome = tk.Label(oponente_frame, text="Oponente:", font=("Arial", 16))
        self.label_oponente_nome.pack()
        self.label_oponente_hp = tk.Label(oponente_frame, text="HP:", font=("Arial", 14))
        self.label_oponente_hp.pack()

        # Lado do Jogador
        jogador_frame = tk.Frame(status_frame)
        jogador_frame.grid(row=1, column=0, sticky="sw", padx=20, pady=20)
        self.label_jogador_nome = tk.Label(jogador_frame, text="Você:", font=("Arial", 16))
        self.label_jogador_nome.pack()
        self.label_jogador_hp = tk.Label(jogador_frame, text="HP:", font=("Arial", 14))
        self.label_jogador_hp.pack()
        self.label_jogador_xp = tk.Label(jogador_frame, text="XP:", font=("Arial", 12))
        self.label_jogador_xp.pack()

        # Menu Inferior
        menu_frame = tk.Frame(self, bd=1, relief="raised", height=150)
        menu_frame.grid(row=1, column=0, sticky="nsew")
        menu_frame.grid_propagate(False)
        menu_frame.columnconfigure(0, weight=3)
        menu_frame.columnconfigure(1, weight=2)
        menu_frame.rowconfigure(0, weight=1)
        
        # Log da Batalha
        log_container = tk.Frame(menu_frame)
        log_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        log_container.rowconfigure(0, weight=1)
        log_container.columnconfigure(0, weight=1)
        log_scrollbar = tk.Scrollbar(log_container)
        log_scrollbar.pack(side="right", fill="y")
        self.log_text = tk.Text(log_container, font=("Arial", 12), wrap="word", state="disabled", yscrollcommand=log_scrollbar.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.config(command=self.log_text.yview)
        
        self.botoes_frame = tk.Frame(menu_frame)
        self.botoes_frame.grid(row=0, column=1, sticky="nsew")
        self.botoes_frame.columnconfigure((0, 1), weight=1) 
        self.botoes_frame.rowconfigure((0, 1), weight=1)
        self.btn_fight = tk.Button(self.botoes_frame, text="LUTAR", font=("Arial", 14),
                                   command=lambda: self.controller.handle_acao_batalha_ginasio(self.batalha_id, 'atacar'))
        self.btn_fight.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.btn_run = tk.Button(self.botoes_frame, text="FUGIR", font=("Arial", 14),
                                 command=lambda: self.controller.handle_acao_batalha_ginasio(self.batalha_id, 'fugir'))
        self.btn_run.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.btn_pokemon = tk.Button(self.botoes_frame, text="POKÉMON", font=("Arial", 14),
                                      command=self.controller.handle_mostrar_tela_troca)
        self.btn_pokemon.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.atualizar_interface(batalha_info)
        
    def atualizar_interface(self, batalha_info):
        equipe_treinador = self.controller.get_treinador_equipe()
        pokemon_em_campo = next((p for p in equipe_treinador if p['id_captura'] == batalha_info['pokemon_em_campo_id_captura']), None)
        
        oponente_lider = batalha_info['oponente_lider']
        pokemon_ativo_idx = oponente_lider['pokemon_ativo_idx']
        pokemon_oponente = oponente_lider['equipe'][pokemon_ativo_idx]
        
        self.label_oponente_nome.config(text=f"Líder {oponente_lider['nome']}: {pokemon_oponente['nome']} (Nv.{pokemon_oponente['nivel']})")
        self.label_oponente_hp.config(text=f"HP: {pokemon_oponente['hp_atual']} / {pokemon_oponente['hp_max']}")

        if pokemon_em_campo:
            self.label_jogador_nome.config(text=f"{pokemon_em_campo['nome']} (Nv.{pokemon_em_campo['nivel']})")
            self.label_jogador_hp.config(text=f"HP: {pokemon_em_campo['hp']} / {pokemon_em_campo['hp_max']}")
            xp_atual = pokemon_em_campo.get('xp_atual', 0)
            xp_para_upar = pokemon_em_campo.get('xp_para_upar', 1)
            self.label_jogador_xp.config(text=f"XP: {xp_atual} / {xp_para_upar}")

            if pokemon_em_campo['hp'] <= 0:
                self.btn_fight.config(state="disabled")
                if hasattr(self, 'btn_run'):
                    self.btn_run.config(state="disabled")
                self.btn_pokemon.config(state="normal", relief="raised")
            else:
                self.btn_fight.config(state="normal")
                if hasattr(self, 'btn_run'):
                    self.btn_run.config(state="normal")
                self.btn_pokemon.config(state="normal")
        
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("1.0", "\n".join(batalha_info['log_batalha']))
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)
        
        if 'resultado_final' in batalha_info:
            for child in self.botoes_frame.winfo_children():
                child.config(state="disabled")