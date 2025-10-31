import tkinter as tk

class TelaBatalha(tk.Frame):
    def __init__(self, master, controller, batalha_info):
        super().__init__(master)
        self.controller = controller
        self.batalha_id = batalha_info['id']

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        status_frame = tk.Frame(self, bd=1, relief="sunken")
        status_frame.grid(row=0, column=0, sticky="nsew")
        
        self.label_oponente = tk.Label(status_frame, text="Oponente:", font=("Arial", 16))
        self.label_oponente.pack(anchor="ne", padx=20, pady=10)

        self.label_jogador = tk.Label(status_frame, text="Você:", font=("Arial", 16))
        self.label_jogador.pack(anchor="sw", padx=20, pady=10)

        menu_frame = tk.Frame(self, bd=1, relief="raised", height=150)
        menu_frame.grid(row=1, column=0, sticky="nsew")
        menu_frame.grid_propagate(False)
        menu_frame.columnconfigure((0, 1), weight=1)
        menu_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(menu_frame, font=("Arial", 12), wrap="word", state="disabled")
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        botoes_frame = tk.Frame(menu_frame)
        botoes_frame.grid(row=0, column=1, sticky="nsew")
        botoes_frame.columnconfigure((0, 1), weight=1)
        botoes_frame.rowconfigure((0, 1), weight=1)
        
        btn_fight = tk.Button(botoes_frame, text="FIGHT", font=("Arial", 14), command=lambda: controller.handle_acao_batalha(self.batalha_id, 'atacar'))
        btn_fight.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        btn_bag = tk.Button(botoes_frame, text="BAG", font=("Arial", 14), command=lambda: controller.handle_acao_batalha(self.batalha_id, 'capturar'))
        btn_bag.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        btn_pokemon = tk.Button(botoes_frame, text="POKÉMON", font=("Arial", 14), command=lambda: controller.mostrar_aviso("Troca ainda não implementada"))
        btn_pokemon.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        btn_run = tk.Button(botoes_frame, text="RUN", font=("Arial", 14), command=lambda: controller.handle_acao_batalha(self.batalha_id, 'fugir'))
        btn_run.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.atualizar_interface(batalha_info)

    def atualizar_interface(self, batalha_info):
        pc_treinador = self.controller.get_treinador_pc()
        pokemon_em_campo = next((p for p in pc_treinador if p['id_captura'] == batalha_info['pokemon_em_campo_id_captura']), None)
        
        oponente = batalha_info['oponente']

        self.label_oponente.config(text=f"{oponente['nome']} (Nv.{oponente['nivel']})")
        self.label_oponente_hp.config(text=f"HP: {oponente['hp_atual']} / {oponente['hp_max']}")
        
        if pokemon_em_campo:
            self.label_jogador_nome.config(text=f"{pokemon_em_campo['nome']} (Nv.{pokemon_em_campo['nivel']})")
            self.label_jogador_hp.config(text=f"HP: {pokemon_em_campo['hp']}")
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("1.0", "\n".join(batalha_info['log_batalha']))
        self.log_text.config(state="disabled")