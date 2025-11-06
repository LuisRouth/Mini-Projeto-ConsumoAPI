import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class TelaBatalha(ctk.CTkFrame):
    def __init__(self, master, controller, batalha_info):
        super().__init__(master)
        self.controller = controller
        self.batalha_id = batalha_info['id']
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.configure(fg_color="#212121")

        # --- Frame de Status do topo ---
        status_frame = ctk.CTkFrame(self, fg_color="#23272b", border_width=0)
        status_frame.place(relx=0, rely=0, relwidth=1, relheight=0.40)

        # --- Oponente (Topo/Direita)
        op_frame = ctk.CTkFrame(status_frame, fg_color="#23272b")
        op_frame.place(relx=0.68, rely=0.10, relwidth=0.3, relheight=0.8)

        self.label_oponente_nome = ctk.CTkLabel(
            op_frame,
            text="Oponente",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        self.label_oponente_nome.pack(pady=(10, 2))

        self.label_oponente_hp = ctk.CTkLabel(
            op_frame,
            text="HP:",
            font=("Arial", 16),
            text_color="#ff5252"
        )
        self.label_oponente_hp.pack()

        # --- Jogador (Baixo/Esquerda)
        jogador_frame = ctk.CTkFrame(status_frame, fg_color="#23272b")
        jogador_frame.place(relx=0.02, rely=0.60, relwidth=0.3, relheight=0.38)

        self.label_jogador_nome = ctk.CTkLabel(
            jogador_frame,
            text="Você:",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        self.label_jogador_nome.pack(pady=(2, 2))

        self.label_jogador_hp = ctk.CTkLabel(
            jogador_frame,
            text="HP:",
            font=("Arial", 16),
            text_color="#ff5252"
        )
        self.label_jogador_hp.pack()

        self.label_jogador_xp = ctk.CTkLabel(
            jogador_frame,
            text="XP:",
            font=("Arial", 13),
            text_color="#b0bec5"
        )
        self.label_jogador_xp.pack()

        # --- Menu/Baixo: Log e Botões ---
        menu_frame = ctk.CTkFrame(self, fg_color="#263238", border_width=0)
        menu_frame.place(relx=0, rely=0.40, relwidth=1, relheight=0.60)

        # Log de batalha com barra de rolagem
        log_container = ctk.CTkFrame(menu_frame, fg_color="#263238")
        log_container.place(relx=0.02, rely=0.06, relwidth=0.61, relheight=0.88)

        self.log_text = ctk.CTkTextbox(
            log_container,
            font=("Arial", 13),
            fg_color="#263238",
            text_color="white",
            state="disabled",
            border_width=1,
            border_color="#c62828"
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        log_scrollbar = ctk.CTkScrollbar(log_container, orientation="vertical", command=self.log_text.yview, fg_color="#c62828")
        log_scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        # --- Botões de ação ---
        self.botoes_frame = ctk.CTkFrame(menu_frame, fg_color="#263238")
        self.botoes_frame.place(relx=0.65, rely=0.06, relwidth=0.33, relheight=0.88)

        self.btn_fight = ctk.CTkButton(
            self.botoes_frame, text="LUTAR",
            font=("Arial", 16, "bold"),
            fg_color="#c62828",
            text_color="white",
            hover_color="#ff5252",
            command=lambda: self.controller.handle_acao_batalha(self.batalha_id, 'atacar')
        )
        self.btn_fight.place(relx=0.03, rely=0.02, relwidth=0.44, relheight=0.44)

        self.btn_bag = ctk.CTkButton(
            self.botoes_frame, text="CAPTURAR",
            font=("Arial", 16, "bold"),
            fg_color="#c62828",
            text_color="white",
            hover_color="#ff5252",
            command=lambda: self.controller.handle_acao_batalha(self.batalha_id, 'capturar')
        )
        self.btn_bag.place(relx=0.53, rely=0.02, relwidth=0.44, relheight=0.44)

        self.btn_pokemon = ctk.CTkButton(
            self.botoes_frame, text="POKÉMON",
            font=("Arial", 16, "bold"),
            fg_color="#c62828",
            text_color="white",
            hover_color="#ff5252",
            command=self.controller.handle_mostrar_tela_troca
        )
        self.btn_pokemon.place(relx=0.03, rely=0.52, relwidth=0.44, relheight=0.44)

        self.btn_run = ctk.CTkButton(
            self.botoes_frame, text="FUGIR",
            font=("Arial", 16, "bold"),
            fg_color="#c62828",
            text_color="white",
            hover_color="#ff5252",
            command=lambda: self.controller.handle_acao_batalha(self.batalha_id, 'fugir')
        )
        self.btn_run.place(relx=0.53, rely=0.52, relwidth=0.44, relheight=0.44)

        self.atualizar_interface(batalha_info)

    def atualizar_interface(self, batalha_info):
        pc_treinador = self.controller.get_treinador_pc()
        equipe_treinador = self.controller.get_treinador_equipe()
        pokemon_em_campo = next((p for p in equipe_treinador if p['id_captura'] == batalha_info['pokemon_em_campo_id_captura']), None)
        oponente = batalha_info['oponente']

        self.label_oponente_nome.configure(text=f"{oponente['nome']} (Nv.{oponente['nivel']})")
        self.label_oponente_hp.configure(text=f"HP: {oponente['hp_atual']} / {oponente['hp_max']}")
        if pokemon_em_campo:
            self.label_jogador_nome.configure(text=f"{pokemon_em_campo['nome']} (Nv.{pokemon_em_campo['nivel']})")
            self.label_jogador_hp.configure(text=f"HP: {pokemon_em_campo['hp']} / {pokemon_em_campo['hp_max']}")
            xp_atual = pokemon_em_campo.get('xp_atual', 0)
            xp_para_upar = pokemon_em_campo.get('xp_para_upar', 1)
            self.label_jogador_xp.configure(text=f"XP: {xp_atual} / {xp_para_upar}")
        else:
            self.label_jogador_nome.configure(text="Erro!")
            self.label_jogador_hp.configure(text="HP: ?? / ??")
            self.label_jogador_xp.configure(text="XP: ?? / ??")

        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("1.0", "\n".join(batalha_info['log_batalha']))
        self.log_text.configure(state="disabled")
        self.log_text.see("end")

        if 'resultado_final' in batalha_info:
            for child in self.botoes_frame.winfo_children():
                child.configure(state="disabled")
