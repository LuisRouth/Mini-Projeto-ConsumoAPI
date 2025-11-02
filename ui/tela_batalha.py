import customtkinter as ctk
from ui.ctk_messagebox import CTkMessageBox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TelaBatalha(ctk.CTkFrame):
    def __init__(self, master, controller, batalha_info):
        super().__init__(master)
        self.controller = controller
        self.batalha_id = batalha_info['id']

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # STATUS Frame
        status_frame = ctk.CTkFrame(self, fg_color="#23272e", corner_radius=12)
        status_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=14)
        status_frame.rowconfigure((0, 1), weight=1)
        status_frame.columnconfigure((0, 1), weight=1)

        # Oponente
        oponente_frame = ctk.CTkFrame(status_frame, fg_color="#2a3136", corner_radius=10)
        oponente_frame.grid(row=0, column=1, sticky="ne", padx=20, pady=20)
        self.label_oponente_nome = ctk.CTkLabel(oponente_frame, text="Oponente:", font=("Arial", 16, "bold"), text_color="#FFD369")
        self.label_oponente_nome.pack()
        self.label_oponente_hp = ctk.CTkLabel(oponente_frame, text="HP:", font=("Arial", 14), text_color="#EEEEEE")
        self.label_oponente_hp.pack()

        # Jogador
        jogador_frame = ctk.CTkFrame(status_frame, fg_color="#2a3136", corner_radius=10)
        jogador_frame.grid(row=1, column=0, sticky="sw", padx=20, pady=20)
        self.label_jogador_nome = ctk.CTkLabel(jogador_frame, text="Você:", font=("Arial", 16, "bold"), text_color="#00adb5")
        self.label_jogador_nome.pack()
        self.label_jogador_hp = ctk.CTkLabel(jogador_frame, text="HP:", font=("Arial", 14), text_color="#EEEEEE")
        self.label_jogador_hp.pack()
        self.label_jogador_xp = ctk.CTkLabel(jogador_frame, text="XP:", font=("Arial", 12), text_color="#FFFFFF")
        self.label_jogador_xp.pack()

        # MENU Frame
        menu_frame = ctk.CTkFrame(self, height=160, fg_color="#23272e", corner_radius=12)
        menu_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        menu_frame.grid_propagate(False)
        menu_frame.columnconfigure(0, weight=3)
        menu_frame.columnconfigure(1, weight=2)
        menu_frame.rowconfigure(0, weight=1)

        # Log Frame
        log_container = ctk.CTkFrame(menu_frame, fg_color="#181c1f", corner_radius=10)
        log_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        log_container.rowconfigure(0, weight=1)
        log_container.columnconfigure(0, weight=1)

        self.log_text = ctk.CTkTextbox(
            log_container,
            font=("Arial", 12),
            state='normal',
            width=280,
            height=120,
            wrap="word",
            fg_color="#181c1f",
            text_color="#FFFFFF",
            corner_radius=8
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        # Botões
        botoes_frame = ctk.CTkFrame(menu_frame, fg_color="#393e46", corner_radius=10)
        botoes_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=10)
        botoes_frame.columnconfigure((0, 1), weight=1)
        botoes_frame.rowconfigure((0, 1), weight=1)

        btn_fight = ctk.CTkButton(
            botoes_frame, text="LUTAR", font=("Arial", 14, "bold"),
            fg_color="#17d43b", hover_color="#14752d",
            corner_radius=14,
            command=lambda: self.controller.handle_acao_batalha(self.batalha_id, 'atacar')
        )
        btn_fight.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        btn_bag = ctk.CTkButton(
            botoes_frame, text="CAPTURAR", font=("Arial", 14, "bold"),
            fg_color="#F8AD19", hover_color="#c7b800",
            corner_radius=14,
            command=lambda: self.controller.handle_acao_batalha(self.batalha_id, 'capturar')
        )
        btn_bag.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        btn_pokemon = ctk.CTkButton(
            botoes_frame, text="POKÉMON", font=("Arial", 14),
            corner_radius=14,
            command=self.controller.handle_mostrar_tela_troca
        )
        btn_pokemon.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        btn_run = ctk.CTkButton(
            botoes_frame, text="FUGIR", font=("Arial", 14, "bold"),
            fg_color="#ff004c", hover_color="#c80035",
            corner_radius=14,
            command=self.mensagem_fuga
        )
        btn_run.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.atualizar_interface(batalha_info)

    def mensagem_fuga(self):
        CTkMessageBox(self, "Ação", "Se você fugir, perderá experiência e não capturará o Pokémon!", icon="warning")
        self.controller.handle_acao_batalha(self.batalha_id, 'fugir')

    def atualizar_interface(self, batalha_info):
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

        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("1.0", "\n".join(batalha_info['log_batalha']))
        self.log_text.configure(state="disabled")
        self.log_text.see("end")
