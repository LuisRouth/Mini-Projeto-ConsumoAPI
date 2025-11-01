import tkinter as tk

class TelaGeral(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Armazena o ID da área que está sendo visualizada no momento
        self.area_selecionada_id = "1"
        
        self.areas_data = self.controller.api_get_areas()
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)
        
        # --- PAINEL DA ESQUERDA ---
        left_panel = tk.Frame(self, padx=10, pady=10)
        left_panel.grid(row=0, column=0, sticky="nsew")

        top_buttons_frame = tk.Frame(left_panel)
        top_buttons_frame.pack(fill="x", pady=10)
        top_buttons_frame.columnconfigure((0, 1, 2), weight=1)
        
        btn_pc = tk.Button(top_buttons_frame, text="Ver PC", font=("Arial", 14), command=self.controller.handle_abrir_pc)
        btn_pc.grid(row=0, column=0, sticky="ew", padx=5)

         # --- SUA EQUIPE ---
        equipe_frame = tk.LabelFrame(left_panel, text="Sua Equipe", font=("Arial", 16), padx=10, pady=10)
        equipe_frame.pack(fill="x", pady=10)
        self.equipe_widgets = []
        self.desenhar_equipe(equipe_frame)

        btn_curar = tk.Button(top_buttons_frame, text="Curar", font=("Arial", 14), command=self.controller.handle_curar_pokemon)
        btn_curar.grid(row=0, column=1, sticky="ew", padx=5)

        btn_salvar = tk.Button(top_buttons_frame, text="Salvar", font=("Arial", 14), command=lambda: self.controller.mostrar_aviso("Salvamento ainda não implementado!"))
        btn_salvar.grid(row=0, column=2, sticky="ew", padx=5)
        
        acoes_frame = tk.LabelFrame(left_panel, text="Ações", font=("Arial", 16), padx=10, pady=10)
        acoes_frame.pack(fill="both", pady=20, expand=True)
        
        ginasios_vencidos = self.controller.get_ginasios_vencidos()
        
        for i, area_id in enumerate(self.areas_data, 1):
            btn = tk.Button(
                acoes_frame,
                text=f"Explorar a Área {area_id}",
                font=("Arial", 12)
            )
            btn.pack(pady=5, fill="x")
            
            if ginasios_vencidos >= (i - 1):
                btn.config(command=lambda aid=area_id: self.mostrar_acoes_padrao(aid))
            else:
                btn.config(state="disabled")

        btn_ginasio = tk.Button(
            acoes_frame,
            text="Ir para o Ginásio",
            font=("Arial", 14),
            command=lambda: self.controller.mostrar_aviso("Ginásio ainda em construção!")
        )
        btn_ginasio.pack(side="bottom", pady=15, fill="x")


        # --- PAINEL DA DIREITA (EVENTOS) ---
        self.eventos_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self.eventos_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.eventos_frame.grid_propagate(False)

        tk.Label(self.eventos_frame, text="Eventos da Área", font=("Arial", 20)).pack(pady=10)
        
        self.log_text_widget = tk.Text(self.eventos_frame, font=("Arial", 14), wrap="word", height=5, bd=0, relief="flat", bg=self.cget("bg"))
        self.log_text_widget.pack(pady=20, padx=20, fill="x")

        self.botoes_acao_frame = tk.Frame(self.eventos_frame)
        self.botoes_acao_frame.pack(side="bottom", pady=20)
        
        # Estado inicial
        self.mostrar_acoes_padrao(self.area_selecionada_id)

    def desenhar_equipe(self, parent_frame):
        for widget in self.equipe_widgets:
            widget.destroy()
        self.equipe_widgets.clear()
        
        equipe = self.controller.get_treinador_equipe()
        
        for i in range(6):
            slot_frame = tk.Frame(parent_frame, bd=2, relief="sunken")
            slot_frame.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.equipe_widgets.append(slot_frame)
            
            placeholder_imagem = tk.Label(slot_frame, text="", bg="white", width=12, height=5)
            placeholder_imagem.pack(padx=5, pady=(5, 0))
            
            nome_label = tk.Label(slot_frame, text="- Vazio -", font=("Arial", 10), fg="gray")
            nome_label.pack(padx=5, pady=(0, 5))
            if i < len(equipe) and equipe[i] is not None:
                pokemon = equipe[i]
                nome_label.config(text=f"{pokemon['nome']} (Nv.{pokemon['nivel']})", fg="black")

    def limpar_botoes_acoes(self):
        for widget in self.botoes_acao_frame.winfo_children():
            widget.destroy()

    def atualizar_info_area(self, area_id):
        for widget in self.botoes_acao_frame.winfo_children():
            widget.destroy()
        area = self.areas_data.get(area_id)
        if not area: return
        
        min_lvl, max_lvl = area["level_range"]
        raridades = ", ".join(area["allowed_rarities"])

        info_texto = (
            f"Você está em: {area['nome']}\n\n"
            f"Nível dos Pokémon: {min_lvl} - {max_lvl}\n"
            f"Raridades encontradas: {raridades}"
        )

        self.log_text_widget.config(state="normal")
        self.log_text_widget.delete("1.0", "end")
        self.log_text_widget.insert("1.0", info_texto)
        self.log_text_widget.config(state="disabled")


    def selecionar_e_explorar_area(self):

        self.controller.handle_procurar_pokemon(self.area_selecionada_id)


    def mostrar_encontro(self, pokemon_encontrado):
        nome = pokemon_encontrado['nome']
        nivel = pokemon_encontrado['nivel']
        tipagem_lista = pokemon_encontrado.get('tipagem', ['Desconhecido'])
        tipo = ", ".join(tipagem_lista)
        raridade = pokemon_encontrado['raridade']

        texto_encontro = (
            f"Um {nome} selvagem apareceu!\n\n"
            f"Nível: {nivel}\n"
            f"Tipo: {tipo}\n"
            f"Raridade: {raridade}"
        )
        
        self.log_text_widget.config(state="normal")
        self.log_text_widget.delete("1.0", "end")
        self.log_text_widget.insert("1.0", texto_encontro)
        self.log_text_widget.config(state="disabled")

        self.limpar_botoes_acoes()
        tk.Button(self.botoes_acao_frame, text="Batalhar", font=("Arial", 12), command=lambda p=pokemon_encontrado: self.controller.handle_iniciar_batalha(p)).pack(side="left", padx=5)
        
        tk.Button(self.botoes_acao_frame, text="Procurar Outro", font=("Arial", 12), command=self.selecionar_e_explorar_area).pack(side="left", padx=5)
        tk.Button(self.botoes_acao_frame, text="Voltar", font=("Arial", 12), command=lambda: self.mostrar_acoes_padrao(self.area_selecionada_id)).pack(side="left", padx=5)
        
    def mostrar_acoes_padrao(self, area_id):
        self.area_selecionada_id = area_id
        self.atualizar_info_area(area_id)
        self.limpar_botoes_acoes()
        
        btn_entrar = tk.Button(
            self.botoes_acao_frame,
            text="Entrar",
            font=("Arial", 16),
            command=self.selecionar_e_explorar_area
        )
        btn_entrar.pack(pady=10)