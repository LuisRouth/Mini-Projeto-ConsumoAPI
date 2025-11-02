import customtkinter as ctk
from ui.ctk_messagebox import CTkMessageBox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TelaGeral(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.area_selecionada_id = "1"
        self.areas_data = self.controller.api_get_areas()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        # PAINEL DA ESQUERDA
        left_panel = ctk.CTkFrame(self, fg_color="#222831", corner_radius=10)
        left_panel.grid(row=0, column=0, sticky="nsew")

        # Top buttons (grid)
        top_buttons_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        top_buttons_frame.grid(row=0, column=0, sticky="ew", pady=(10,0))
        for i in range(3):
            top_buttons_frame.columnconfigure(i, weight=1)

        ctk.CTkButton(top_buttons_frame, text="Ver PC", font=("Arial", 14, "bold"),
                      command=self.controller.handle_abrir_pc, corner_radius=12,
                      fg_color="#00adb5", hover_color="#393e46")\
            .grid(row=0, column=0, sticky="ew", padx=5)
        ctk.CTkButton(top_buttons_frame, text="Curar", font=("Arial", 14, "bold"),
                      command=self.controller.handle_curar_pokemon, corner_radius=12,
                      fg_color="#F8AD19", hover_color="#00adb5")\
            .grid(row=0, column=1, sticky="ew", padx=5)
        ctk.CTkButton(top_buttons_frame, text="Salvar", font=("Arial", 14),
                      command=lambda: CTkMessageBox(self, "Função não implementada", "Salvamento ainda não implementado!", icon="warning"),
                      corner_radius=12, fg_color="#8877dd")\
            .grid(row=0, column=2, sticky="ew", padx=5)

        # Equipe (grid ONLY)
        equipe_frame = ctk.CTkFrame(left_panel, fg_color="#23272e", corner_radius=12)
        equipe_frame.grid(row=1, column=0, sticky="new", pady=10)
        ctk.CTkLabel(equipe_frame, text="Sua Equipe", font=("Arial", 16, "bold"), text_color="#FFD369")\
            .grid(row=0, column=0, columnspan=3, pady=(3,8), sticky="ew")
        self.equipe_widgets = []
        self.desenhar_equipe(equipe_frame)

        # Ações (grid)
        acoes_frame = ctk.CTkFrame(left_panel, fg_color="#393e46", corner_radius=12)
        acoes_frame.grid(row=2, column=0, sticky="nsew", pady=(12,4), padx=0)
        ginasios_vencidos = self.controller.get_ginasios_vencidos()
        for i, area_id in enumerate(self.areas_data, 1):
            btn = ctk.CTkButton(
                acoes_frame,
                text=f"Explorar a Área {area_id}", font=("Arial", 12),
                width=180, fg_color="#00adb5"
            )
            btn.grid(row=i, column=0, sticky="ew", padx=16, pady=4)
            if ginasios_vencidos >= (i - 1):
                btn.configure(command=lambda aid=area_id: self.mostrar_acoes_padrao(aid))
            else:
                btn.configure(state="disabled", fg_color="#444444")
        ctk.CTkButton(
            acoes_frame, text="Ir para o Ginásio", font=("Arial", 14, "bold"),
            corner_radius=14, fg_color="#F8AD19",
            command=lambda: CTkMessageBox(self, "Função não implementada", "Ginásio ainda em construção!", icon="warning")
        ).grid(row=99, column=0, sticky="ew", padx=16, pady=15)

        # PAINEL DA DIREITA (EVENTOS)
        self.eventos_frame = ctk.CTkFrame(self, fg_color="#23272e", corner_radius=12)
        self.eventos_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.eventos_frame.grid_propagate(False)

        ctk.CTkLabel(self.eventos_frame, text="Eventos da Área", font=("Arial", 20, "bold"),
                     text_color="#F8AD19").pack(pady=10)
        self.log_text_widget = ctk.CTkTextbox(
            self.eventos_frame, font=("Arial", 14), wrap="word", height=90, corner_radius=12,
            fg_color="#393e46", text_color="#EEEEEE"
        )
        self.log_text_widget.pack(pady=20, padx=20, fill="x")
        self.botoes_acao_frame = ctk.CTkFrame(self.eventos_frame, fg_color="transparent")
        self.botoes_acao_frame.pack(side="bottom", pady=20)

        self.mostrar_acoes_padrao(self.area_selecionada_id)

    def desenhar_equipe(self, parent_frame):
        for widget in self.equipe_widgets:
            widget.destroy()
        self.equipe_widgets.clear()
        equipe = self.controller.get_treinador_equipe()
        for i in range(6):
            slot_frame = ctk.CTkFrame(parent_frame, fg_color="#393e46", corner_radius=7)
            slot_frame.grid(row=1 + i // 3, column=i % 3, padx=5, pady=5)
            self.equipe_widgets.append(slot_frame)
            placeholder_imagem = ctk.CTkLabel(
                slot_frame, text="", fg_color="#EEEEEE", width=40, height=20)
            placeholder_imagem.pack(padx=5, pady=(5, 0))
            nome_label = ctk.CTkLabel(
                slot_frame, text="- Vazio -", font=("Arial", 10), text_color="#888888")
            nome_label.pack(padx=5, pady=(0, 5))
            if i < len(equipe) and equipe[i] is not None:
                pk = equipe[i]
                nome_label.configure(text=f"{pk['nome']} (Nv.{pk['nivel']})", text_color="#F8AD19")

    def limpar_botoes_acoes(self):
        for widget in self.botoes_acao_frame.winfo_children():
            widget.destroy()

    def atualizar_info_area(self, area_id):
        area = self.areas_data.get(area_id)
        if not area: return
        min_lvl, max_lvl = area["level_range"]
        raridades = ", ".join(area["allowed_rarities"])
        info_texto = (f"Você está em: {area['nome']}\n\n"
                      f"Nível dos Pokémon: {min_lvl} - {max_lvl}\n"
                      f"Raridades encontradas: {raridades}")
        self.log_text_widget.configure(state="normal")
        self.log_text_widget.delete("1.0", "end")
        self.log_text_widget.insert("1.0", info_texto)
        self.log_text_widget.configure(state="disabled")

    def selecionar_e_explorar_area(self):
        self.controller.handle_procurar_pokemon(self.area_selecionada_id)

    def mostrar_encontro(self, pokemon_encontrado):
        nome = pokemon_encontrado['nome']
        nivel = pokemon_encontrado['nivel']
        tipagem_lista = pokemon_encontrado.get('tipagem', ['Desconhecido'])
        tipo = ", ".join(tipagem_lista)
        raridade = pokemon_encontrado['raridade']
        texto_encontro = (f"Um {nome} selvagem apareceu!\n\n"
                          f"Nível: {nivel}\n"
                          f"Tipo: {tipo}\n"
                          f"Raridade: {raridade}")
        self.log_text_widget.configure(state="normal")
        self.log_text_widget.delete("1.0", "end")
        self.log_text_widget.insert("1.0", texto_encontro)
        self.log_text_widget.configure(state="disabled")
        self.limpar_botoes_acoes()
        ctk.CTkButton(
            self.botoes_acao_frame, text="Batalhar", font=("Arial", 12),
            command=lambda p=pokemon_encontrado: self.controller.handle_iniciar_batalha(p),
            corner_radius=13, fg_color="#00adb5"
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            self.botoes_acao_frame, text="Procurar Outro", font=("Arial", 12),
            command=self.selecionar_e_explorar_area, corner_radius=13, fg_color="#F8AD19"
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            self.botoes_acao_frame, text="Voltar", font=("Arial", 12),
            command=lambda: self.mostrar_acoes_padrao(self.area_selecionada_id), corner_radius=13, fg_color="#393e46"
        ).pack(side="left", padx=5)

    def mostrar_acoes_padrao(self, area_id):
        self.area_selecionada_id = area_id
        self.atualizar_info_area(area_id)
        self.limpar_botoes_acoes()
        ctk.CTkButton(
            self.botoes_acao_frame, text="Entrar", font=("Arial", 16, "bold"),
            command=self.selecionar_e_explorar_area, corner_radius=14, fg_color="#00adb5"
        ).pack(pady=10)
