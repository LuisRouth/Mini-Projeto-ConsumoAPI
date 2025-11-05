import tkinter as tk

class TelaGeral(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Armazena o ID da área que está sendo visualizada no momento
        self.area_selecionada_id = "1"
        
        self.areas_data = self.controller.api_get_areas()
        
<<<<<<< Updated upstream
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
=======
        # --- CORREÇÃO ANTI-TRAVAMENTO: Variáveis de estado ---
        self._last_bg_width = 0
        self._last_bg_height = 0


        # --- PAINEL ESQUERDO ---
        left_panel = ctk.CTkFrame(self, fg_color="#23272b")
        left_panel.place(relx=0, rely=0, relwidth=0.38, relheight=1)

        # Top buttons
        top_buttons_frame = ctk.CTkFrame(left_panel, fg_color="#23272b")
        top_buttons_frame.pack(fill="x", padx=12, pady=12)

        self.btn_pc = ctk.CTkButton(top_buttons_frame, text="Ver PC", font=("Arial", 14, "bold"),
                                    fg_color="#c62828", text_color="white", hover_color="#ff5252",
                                    command=self.controller.handle_abrir_pc)
        self.btn_pc.pack(side="left", padx=5, expand=True, fill="x")
        self.btn_curar = ctk.CTkButton(top_buttons_frame, text="Curar", font=("Arial", 14, "bold"),
                                       fg_color="#c62828", text_color="white", hover_color="#ff5252",
                                       command=self.controller.handle_curar_pokemon)
        self.btn_curar.pack(side="left", padx=5, expand=True, fill="x")
        self.btn_salvar = ctk.CTkButton(top_buttons_frame, text="Salvar", font=("Arial", 14, "bold"),
                                        fg_color="#b71c1c", text_color="white", hover_color="#ff5252",
                                        command=lambda: self.mostrar_aviso_padrao("Salvamento ainda não implementado!", tipo="info"))
        self.btn_salvar.pack(side="left", padx=5, expand=True, fill="x")

        # --- CORREÇÃO APLICADA AQUI ---
        # A variável 'equipe_container' agora é salva como 'self.equipe_container'
        self.equipe_container = ctk.CTkFrame(left_panel, fg_color="#263238")
        self.equipe_container.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(self.equipe_container, text="Sua Equipe", font=("Arial", 16, "bold"), text_color="white", anchor="w").pack(pady=4, anchor="w")
        # --- FIM DA CORREÇÃO ---
        
        self.equipe_widgets = []
        self.frame_grid = None
        self.desenhar_equipe(self.equipe_container) # Agora usa a variável self
>>>>>>> Stashed changes

        btn_curar = tk.Button(top_buttons_frame, text="Curar", font=("Arial", 14), command=self.controller.handle_curar_pokemon)
        btn_curar.grid(row=0, column=1, sticky="ew", padx=5)

        btn_salvar = tk.Button(top_buttons_frame, text="Salvar", font=("Arial", 14), command=lambda: self.controller.mostrar_aviso("Salvamento ainda não implementado!"))
        btn_salvar.grid(row=0, column=2, sticky="ew", padx=5)
        
        acoes_frame = tk.LabelFrame(left_panel, text="Ações", font=("Arial", 16), padx=10, pady=10)
        acoes_frame.pack(fill="both", pady=20, expand=True)
        
        ginasios_vencidos = self.controller.get_ginasios_vencidos()
        
        # Iteramos por todas as áreas disponíveis
        for area_id, area_info in self.areas_data.items():
            # Frame para agrupar os botões de cada área
            area_container = tk.LabelFrame(acoes_frame, text=area_info['nome'], font=("Arial", 14), padx=10, pady=5)
            area_container.pack(fill="x", pady=7)
            
            # Botão de Explorar (procurar Pokémon selvagens)
            btn_explorar = tk.Button(
                area_container,
                text="Explorar Área",
                font=("Arial", 12),
                command=lambda aid=area_id: self.mostrar_acoes_padrao(aid)
            )
            btn_explorar.pack(side="left", padx=5, expand=True)

            # Botão de Ginásio (com a nova lógica)
            btn_ginasio = tk.Button(
                area_container,
                font=("Arial", 12, "bold"),
            )
            btn_ginasio.pack(side="left", padx=5, expand=True)
            
            # --- LÓGICA DE PROGRESSÃO ---
            area_num = int(area_id)

            if ginasios_vencidos >= area_num:
                # O jogador JÁ venceu este ginásio
                area_container.config(fg="gray")
                btn_ginasio.config(text="Ginásio Vencido", state="disabled")
                btn_explorar.config(state="normal")
            
            elif ginasios_vencidos == area_num - 1:
                # Esta é a área ATUAL do jogador
                area_container.config(fg="blue")
                btn_ginasio.config(text="Desafiar Ginásio", state="normal",
                                   command=lambda gid=area_id: self.controller.handle_desafiar_ginasio(gid))
                btn_explorar.config(state="normal")
                
            else:
                # Áreas futuras que estão bloqueadas
                area_container.config(fg="gray")
                btn_ginasio.config(text="Ginásio Bloqueado", state="disabled")
                btn_explorar.config(state="disabled")

<<<<<<< Updated upstream

        # --- PAINEL DA DIREITA (EVENTOS) ---
        self.eventos_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self.eventos_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.eventos_frame.grid_propagate(False)

        tk.Label(self.eventos_frame, text="Eventos da Área", font=("Arial", 20)).pack(pady=10)
=======
        # --- PAINEL DIREITO ---
>>>>>>> Stashed changes
        
        self.log_text_widget = tk.Text(self.eventos_frame, font=("Arial", 14), wrap="word", height=5, bd=0, relief="flat", bg=self.cget("bg"))
        self.log_text_widget.pack(pady=20, padx=20, fill="x")

<<<<<<< Updated upstream
        self.botoes_acao_frame = tk.Frame(self.eventos_frame)
        self.botoes_acao_frame.pack(side="bottom", pady=20)
        
        # Estado inicial
        self.mostrar_acoes_padrao(self.area_selecionada_id)
=======
        self.nomes_imagens_fundo = {
            "1": "Rota_Inicial.png",
            "2": "Floresta_Sombria.png",
            "3": "Montanha_Rochosa.png",
            "4": "Caverna_Misteriosa.png"
        }
        self.imagens_fundo_pil = {}
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # pasta raiz
        
        for area_id, nome_arquivo in self.nomes_imagens_fundo.items():
            try:
                # Corrigindo o caminho da imagem para a pasta 'imagens'
                image_path = os.path.join(base_dir, "imagens", nome_arquivo) 
                self.imagens_fundo_pil[area_id] = Image.open(image_path)
            except Exception as e:
                print(f"Erro ao carregar imagem {nome_arquivo}: {e}")
                self.imagens_fundo_pil[area_id] = None 

        self.pil_bg_image_selecionada = self.imagens_fundo_pil.get(self.area_selecionada_id)

        self.bg_image_label = ctk.CTkLabel(self.eventos_frame, text="", fg_color="transparent")
        self.bg_image_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        if self.pil_bg_image_selecionada:
             self.eventos_frame.bind("<Configure>", self._redesenhar_imagem_fundo)
        
        ctk.CTkLabel(self.eventos_frame, text="Eventos da Área", font=("Arial", 20, "bold"), text_color="white", fg_color="transparent").place(relx=0.5, rely=0.05, anchor="center")

        self.log_text_widget = ctk.CTkTextbox(self.eventos_frame, font=("Arial", 14),
                                              fg_color="#212121", text_color="white",
                                              border_color="#c62828", border_width=2)
        
        self.log_text_widget.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.25) 

        self.botoes_acao_frame = ctk.CTkFrame(self.eventos_frame, fg_color="transparent")
        self.botoes_acao_frame.place(relx=0.5, rely=0.45, anchor="n") 

        self.mostrar_acoes_padrao(self.area_selecionada_id)
        self.after(100, self._redesenhar_imagem_fundo) 

    # --- FUNÇÃO DE REDIMENSIONAMENTO (Com correção anti-travamento) ---
    def _redesenhar_imagem_fundo(self, event=None):
        if not self.pil_bg_image_selecionada:
            self.bg_image_label.configure(image=None)
            return
        
        width = self.eventos_frame.winfo_width()
        height = self.eventos_frame.winfo_height()

        if width <= 1 or height <= 1:
            return
        # Proteção contra loop infinito:
        if width == self._last_bg_width and height == self._last_bg_height:
            return

        self._last_bg_width = width
        self._last_bg_height = height
        
        self.bg_image_resized = ctk.CTkImage(self.pil_bg_image_selecionada, size=(width, height))
        self.bg_image_label.configure(image=self.bg_image_resized)

    # --- Funções restantes ---

    def mostrar_aviso_padrao(self, mensagem, tipo="info", titulo="Aviso"):
        PopupPadrao(self, mensagem, titulo, tipo)
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
=======

        nova_imagem = self.imagens_fundo_pil.get(area_id)
        if nova_imagem:
            self.pil_bg_image_selecionada = nova_imagem
            self._redesenhar_imagem_fundo()
        else:
            self.pil_bg_image_selecionada = None
            self._redesenhar_imagem_fundo()
        
>>>>>>> Stashed changes
        self.atualizar_info_area(area_id)
        self.limpar_botoes_acoes()
        
        btn_entrar = tk.Button(
            self.botoes_acao_frame,
            text="Entrar",
            font=("Arial", 16),
            command=self.selecionar_e_explorar_area
        )
        btn_entrar.pack(pady=10)