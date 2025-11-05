from .popup_padrao import PopupPadrao
import customtkinter as ctk
import os  # Necessário para construir o caminho da imagem
from PIL import Image  # Necessário para carregar a imagem

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class TelaGeral(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.configure(fg_color="#212121")

        self.area_selecionada_id = "1"
        self.areas_data = self.controller.api_get_areas()

        # --- PAINEL ESQUERDO (Sem alterações) ---
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

        # Equipe Pokémon
        equipe_container = ctk.CTkFrame(left_panel, fg_color="#263238")
        equipe_container.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(equipe_container, text="Sua Equipe", font=("Arial", 16, "bold"), text_color="white", anchor="w").pack(pady=4, anchor="w")
        self.equipe_widgets = []
        self.frame_grid = None
        self.desenhar_equipe(equipe_container)

        # Painel de ações (Scrollable)
        acoes_frame = ctk.CTkScrollableFrame(
            left_panel, 
            fg_color="#23272b",
            label_text="Ações",
            label_font=("Arial", 16, "bold"),
            label_text_color="#c62828"
        )
        acoes_frame.pack(fill="both", pady=18, padx=10, expand=True)
        
        ginasios_vencidos = self.controller.get_ginasios_vencidos()
        for area_id, area_info in self.areas_data.items():
            area_container = ctk.CTkFrame(acoes_frame, fg_color="#262626", border_color="#c62828", border_width=2)
            area_container.pack(fill="x", pady=5, padx=3)

            lbl = ctk.CTkLabel(area_container, text=area_info['nome'], font=("Arial", 14, "bold"), text_color="white")
            lbl.pack(anchor="w", pady=3)

            btn_explorar = ctk.CTkButton(area_container, text="Explorar Área", font=("Arial", 12),
                                         fg_color="#c62828", text_color="white", hover_color="#ff5252",
                                         command=lambda aid=area_id: self.mostrar_acoes_padrao(aid))
            btn_explorar.pack(side="left", padx=5, pady=5, expand=True)
            btn_ginasio = ctk.CTkButton(area_container, font=("Arial", 12, "bold"),
                                        fg_color="#b71c1c", text_color="white", hover_color="#ff5252")
            btn_ginasio.pack(side="left", padx=5, pady=5, expand=True)

            area_num = int(area_id)
            if ginasios_vencidos >= area_num:
                btn_ginasio.configure(text="Ginásio Vencido", state="disabled")
                btn_explorar.configure(state="normal")
                area_container.configure(border_color="gray")
            elif ginasios_vencidos == area_num - 1:
                btn_ginasio.configure(text="Desafiar Ginásio", state="normal", command=lambda gid=area_id: self.controller.handle_desafiar_ginasio(gid))
                btn_explorar.configure(state="normal")
                area_container.configure(border_color="#2196f3")
            else:
                btn_ginasio.configure(text="Ginásio Bloqueado", state="disabled")
                btn_explorar.configure(state="disabled")
                area_container.configure(border_color="gray")

        # --- PAINEL DIREITO (MODIFICADO) ---
        
        self.eventos_frame = ctk.CTkFrame(self, fg_color="transparent", border_width=2, border_color="#c62828")
        self.eventos_frame.place(relx=0.38, rely=0, relwidth=0.62, relheight=1)

        # --- MODIFICAÇÃO: Carregar todas as imagens de fundo ---
        self.nomes_imagens_fundo = {
            "1": "Rota_Inicial.png",
            "2": "Floresta_Sombria.png",
            "3": "Montanha_Rochosa.png",
            "4": "Caverna_Misteriosa.png" # Supondo que o ID da Caverna é "4"
        }
        self.imagens_fundo_pil = {}
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # pasta raiz
        
        for area_id, nome_arquivo in self.nomes_imagens_fundo.items():
            try:
                image_path = os.path.join(base_dir, "imagens", nome_arquivo)
                self.imagens_fundo_pil[area_id] = Image.open(image_path)
            except Exception as e:
                print(f"Erro ao carregar imagem {nome_arquivo}: {e}")
                self.imagens_fundo_pil[area_id] = None # Fallback

        # Define a imagem de fundo inicial
        self.pil_bg_image_selecionada = self.imagens_fundo_pil.get(self.area_selecionada_id)
        # --- FIM DA MODIFICAÇÃO ---

        self.bg_image_label = ctk.CTkLabel(self.eventos_frame, text="", fg_color="transparent")
        self.bg_image_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Bind (ligação) para a função de redimensionamento
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
        # Garantir que a imagem inicial seja desenhada corretamente
        self.after(100, self._redesenhar_imagem_fundo) 

    # --- FUNÇÃO DE REDIMENSIONAMENTO MODIFICADA ---
    def _redesenhar_imagem_fundo(self, event=None):
        """Pega a imagem de fundo 'selecionada' e a redimensiona para o frame."""
        if not self.pil_bg_image_selecionada:
            return
        
        width = self.eventos_frame.winfo_width()
        height = self.eventos_frame.winfo_height()

        # Evita erro se o frame ainda não tiver tamanho (width=1)
        if width <= 1 or height <= 1:
            return
        
        self.bg_image_resized = ctk.CTkImage(self.pil_bg_image_selecionada, size=(width, height))
        self.bg_image_label.configure(image=self.bg_image_resized)

    # --- Funções restantes ---

    def mostrar_aviso_padrao(self, mensagem, tipo="info", titulo="Aviso"):
        PopupPadrao(self, mensagem, titulo, tipo)

    def desenhar_equipe(self, parent_frame):
        for widget in self.equipe_widgets:
            widget.destroy()
        self.equipe_widgets.clear()

        if self.frame_grid is not None and self.frame_grid.winfo_exists():
            self.frame_grid.destroy()
        self.frame_grid = ctk.CTkFrame(parent_frame, fg_color="#263238")
        self.frame_grid.pack(padx=4, pady=4, fill="x")

        self.frame_grid.columnconfigure((0,1,2), weight=1)

        equipe = self.controller.get_treinador_equipe()
        for i in range(6):
            slot_frame = ctk.CTkFrame(
                self.frame_grid,
                fg_color="#263238",
                border_color="#c62828",
                border_width=2,
                corner_radius=7,
                width=115,
                height=62
            )
            slot_frame.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            self.equipe_widgets.append(slot_frame)
            placeholder_imagem = ctk.CTkLabel(
                slot_frame,
                text="🕹️",
                fg_color="#c62828",
                text_color="white",
                width=60,
                height=30,
                font=("Arial", 20)
            )
            placeholder_imagem.pack(padx=2, pady=(8, 3))
            nome_label = ctk.CTkLabel(
                slot_frame,
                text="- Vazio -",
                font=("Arial", 11),
                text_color="gray",
                fg_color="#263238"
            )
            nome_label.pack(pady=(0, 7))
            if i < len(equipe) and equipe[i] is not None:
                pokemon = equipe[i]
                nome_label.configure(text=f"{pokemon['nome']} (Nv.{pokemon['nivel']})", text_color="white")

    def limpar_botoes_acoes(self):
        for widget in self.botoes_acao_frame.winfo_children():
            widget.destroy()

    def atualizar_info_area(self, area_id):
        area = self.areas_data.get(area_id)
        if not area:
            return
        min_lvl, max_lvl = area["level_range"]
        raridades = ", ".join(area["allowed_rarities"])
        info_texto = (
            f"Você está em: {area['nome']}\n\n"
            f"Nível dos Pokémon: {min_lvl} - {max_lvl}\n"
            f"Raridades encontradas: {raridades}"
        )
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
        texto_encontro = (
            f"Um {nome} selvagem apareceu!\n\n"
            f"Nível: {nivel}\n"
            f"Tipo: {tipo}\n"
            f"Raridade: {raridade}"
        )
        self.log_text_widget.configure(state="normal")
        self.log_text_widget.delete("1.0", "end")
        self.log_text_widget.insert("1.0", texto_encontro)
        self.log_text_widget.configure(state="disabled")
        self.limpar_botoes_acoes()
        ctk.CTkButton(self.botoes_acao_frame, text="Batalhar", font=("Arial", 14),
                      fg_color="#c62828", text_color="white", hover_color="#ff5252",
                      command=lambda p=pokemon_encontrado: self.controller.handle_iniciar_batalha(p)).pack(side="left", padx=5)
        ctk.CTkButton(self.botoes_acao_frame, text="Procurar Outro", font=("Arial", 14),
                      fg_color="#b71c1c", text_color="white", hover_color="#ff5252",
                      command=self.selecionar_e_explorar_area).pack(side="left", padx=5)
        ctk.CTkButton(self.botoes_acao_frame, text="Voltar", font=("Arial", 14),
                      fg_color="#263238", text_color="white", hover_color="#ff5252",
                      command=lambda: self.mostrar_acoes_padrao(self.area_selecionada_id)).pack(side="left", padx=5)

    def mostrar_acoes_padrao(self, area_id):
        self.area_selecionada_id = area_id

        # --- MODIFICAÇÃO: Trocar a imagem de fundo ---
        nova_imagem = self.imagens_fundo_pil.get(area_id)
        if nova_imagem:
            self.pil_bg_image_selecionada = nova_imagem
            self._redesenhar_imagem_fundo() # Força o redesenho
        # --- FIM DA MODIFICAÇÃO ---
        
        self.atualizar_info_area(area_id)
        self.limpar_botoes_acoes()
        ctk.CTkButton(
            self.botoes_acao_frame,
            text="Entrar",
            font=("Arial", 16),
            fg_color="#c62828",
            text_color="white",
            hover_color="#ff5252",
            command=self.selecionar_e_explorar_area
        ).pack(pady=10)