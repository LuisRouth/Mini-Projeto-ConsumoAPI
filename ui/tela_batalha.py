<<<<<<< Updated upstream
import tkinter as tk

class TelaBatalha(tk.Frame):
=======
import customtkinter as ctk
import os  # Importado para imagens
from PIL import Image  # Importado para imagens

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class TelaBatalha(ctk.CTkFrame):
>>>>>>> Stashed changes
    def __init__(self, master, controller, batalha_info):
        super().__init__(master)
        self.controller = controller
        self.batalha_id = batalha_info['id']
<<<<<<< Updated upstream

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        status_frame = tk.Frame(self, bd=1, relief="sunken")
        status_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configura o frame de status para usar grid (2 linhas, 2 colunas)
        status_frame.rowconfigure((0, 1), weight=1)
        status_frame.columnconfigure((0, 1), weight=1)

        # --- Lado do Oponente (Posicionado na Linha 0, Coluna 1 - Canto Superior Direito) ---
        oponente_frame = tk.Frame(status_frame)
        oponente_frame.grid(row=0, column=1, sticky="ne", padx=20, pady=20) # Aumentei pady para 20

        self.label_oponente_nome = tk.Label(oponente_frame, text="Oponente:", font=("Arial", 16))
        self.label_oponente_nome.pack()
        self.label_oponente_hp = tk.Label(oponente_frame, text="HP:", font=("Arial", 14))
        self.label_oponente_hp.pack()

        # --- Lado do Jogador (Posicionado na Linha 1, Coluna 0 - Canto Inferior Esquerdo) ---
        jogador_frame = tk.Frame(status_frame)
        jogador_frame.grid(row=1, column=0, sticky="sw", padx=20, pady=20) # Aumentei pady para 20

        self.label_jogador_nome = tk.Label(jogador_frame, text="Você:", font=("Arial", 16))
        self.label_jogador_nome.pack()
        self.label_jogador_hp = tk.Label(jogador_frame, text="HP:", font=("Arial", 14))
        self.label_jogador_hp.pack()
        self.label_jogador_xp = tk.Label(jogador_frame, text="XP:", font=("Arial", 12))
        self.label_jogador_xp.pack()

        menu_frame = tk.Frame(self, bd=1, relief="raised", height=150)
        menu_frame.grid(row=1, column=0, sticky="nsew")
        menu_frame.grid_propagate(False)
        menu_frame.columnconfigure(0, weight=3)
        menu_frame.columnconfigure(1, weight=2)
        menu_frame.rowconfigure(0, weight=1)
        
        # --- Frame para o Log com Scrollbar ---
        log_container = tk.Frame(menu_frame)
        log_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        log_container.rowconfigure(0, weight=1)
        log_container.columnconfigure(0, weight=1)

        log_scrollbar = tk.Scrollbar(log_container)
        log_scrollbar.pack(side="right", fill="y")
        
        self.log_text = tk.Text(
            log_container, 
            font=("Arial", 12), 
            wrap="word", 
=======
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.configure(fg_color="#212121")

        # --- CORREÇÃO ANTI-TRAVAMENTO: Variáveis de estado ---
        self._last_bg_width = 0
        self._last_bg_height = 0

        # --- Frame de Status do topo ---
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent", border_width=0)
        self.status_frame.place(relx=0, rely=0, relwidth=1, relheight=0.65)

        # --- Bloco de Imagem de Fundo (Batalha Padrão) ---
        self.pil_bg_image = None
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # pasta raiz
            image_path = os.path.join(base_dir, "imagens", "Battle_BackGround .png") 
            self.pil_bg_image = Image.open(image_path)
        except Exception as e:
            print(f"Erro ao carregar imagem Battle_BackGround .png: {e}")
        
        self.bg_image_label = ctk.CTkLabel(self.status_frame, text="", fg_color="transparent")
        self.bg_image_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        if self.pil_bg_image:
                self.status_frame.bind("<Configure>", self._redesenhar_imagem_fundo)
        # --- FIM DO BLOCO DE IMAGEM ---

        # --- Oponente (Topo/Direita)
        op_frame = ctk.CTkFrame(self.status_frame, fg_color="transparent", border_width=1, border_color="#c62828", height=100)
        op_frame.place(relx=0.68, rely=0.10, relwidth=0.3)

        self.label_oponente_nome = ctk.CTkLabel(op_frame, text="Oponente", font=("Arial", 20, "bold"), text_color="white")
        self.label_oponente_nome.pack(pady=5, padx=5, expand=True)

        self.label_oponente_hp = ctk.CTkLabel(op_frame, text="HP:", font=("Arial", 16), text_color="#ff5252")
        self.label_oponente_hp.pack(pady=5, padx=5, expand=True)

        # --- Jogador (Baixo/Esquerda)
        jogador_frame = ctk.CTkFrame(self.status_frame, fg_color="transparent", border_width=1, border_color="#c62828", height=100)
        jogador_frame.place(relx=0.02, rely=0.65, relwidth=0.3)

        self.label_jogador_nome = ctk.CTkLabel(jogador_frame, text="Você:", font=("Arial", 20, "bold"), text_color="white")
        self.label_jogador_nome.pack(pady=2, padx=5)

        self.label_jogador_hp = ctk.CTkLabel(jogador_frame, text="HP:", font=("Arial", 16), text_color="#ff5252")
        self.label_jogador_hp.pack(pady=2, padx=5)

        self.label_jogador_xp = ctk.CTkLabel(jogador_frame, text="XP:", font=("Arial", 13), text_color="#b0bec5")
        self.label_jogador_xp.pack(pady=2, padx=5)

        # --- Menu/Baixo: Log e Botões ---
        menu_frame = ctk.CTkFrame(self, fg_color="#263238", border_width=0)
        menu_frame.place(relx=0, rely=0.65, relwidth=1, relheight=0.35)
        
        menu_frame.grid_columnconfigure(0, weight=6) # 60% para log
        menu_frame.grid_columnconfigure(1, weight=4) # 40% para botões
        menu_frame.grid_rowconfigure(0, weight=1)

        # Log de batalha com barra de rolagem
        log_container = ctk.CTkFrame(menu_frame, fg_color="#263238")
        log_container.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        self.log_text = ctk.CTkTextbox(
            log_container,
            font=("Arial", 13),
            fg_color="#263238",
            text_color="white",
>>>>>>> Stashed changes
            state="disabled",
            yscrollcommand=log_scrollbar.set
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.config(command=self.log_text.yview)
        
        # --- Frame para os Botões ---
        self.botoes_frame = tk.Frame(menu_frame)
        self.botoes_frame.grid(row=0, column=1, sticky="nsew")
        self.botoes_frame.columnconfigure((0, 1), weight=1)
        self.botoes_frame.rowconfigure((0, 1), weight=1)

        # --- Botões ---
        self.btn_fight = tk.Button(self.botoes_frame, text="LUTAR", font=("Arial", 14), command=lambda: self.controller.handle_acao_batalha(self.batalha_id, 'atacar'))
        self.btn_fight.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

<<<<<<< Updated upstream
        self.btn_bag = tk.Button(self.botoes_frame, text="CAPTURAR", font=("Arial", 14), command=lambda: self.controller.handle_acao_batalha(self.batalha_id, 'capturar'))
        self.btn_bag.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        self.btn_pokemon = tk.Button(self.botoes_frame, text="POKÉMON", font=("Arial", 14), command=self.controller.handle_mostrar_tela_troca)
        self.btn_pokemon.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.btn_run = tk.Button(self.botoes_frame, text="FUGIR", font=("Arial", 14), command=lambda: self.controller.handle_acao_batalha(self.batalha_id, 'fugir'))
        self.btn_run.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
=======
        # --- Botões de ação ---
        self.botoes_frame = ctk.CTkFrame(menu_frame, fg_color="#263238")
        self.botoes_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        
        self.botoes_frame.grid_columnconfigure((0, 1), weight=1)
        self.botoes_frame.grid_rowconfigure((0, 1), weight=1)

        self.btn_fight = ctk.CTkButton(
            self.botoes_frame, text="LUTAR",
            font=("Arial", 16, "bold"),
            fg_color="#c62828",
            text_color="white",
            hover_color="#ff5252",
            command=lambda: self.controller.handle_acao_batalha(self.batalha_id, 'atacar')
        )
        self.btn_fight.grid(row=0, column=0, padx=5, pady=5) 

        self.btn_bag = ctk.CTkButton(
            self.botoes_frame, text="CAPTURAR",
            font=("Arial", 16, "bold"),
            fg_color="#c62828",
            text_color="white",
            hover_color="#ff5252",
            command=lambda: self.controller.handle_acao_batalha(self.batalha_id, 'capturar')
        )
        self.btn_bag.grid(row=0, column=1, padx=5, pady=5)

        self.btn_pokemon = ctk.CTkButton(
            self.botoes_frame, text="POKÉMON",
            font=("Arial", 16, "bold"),
            fg_color="#c62828",
            text_color="white",
            hover_color="#ff5252",
            command=self.controller.handle_mostrar_tela_troca
        )
        self.btn_pokemon.grid(row=1, column=0, padx=5, pady=5)

        self.btn_run = ctk.CTkButton(
            self.botoes_frame, text="FUGIR",
            font=("Arial", 16, "bold"),
            fg_color="#c62828",
            text_color="white",
            hover_color="#ff5252",
            command=lambda: self.controller.handle_acao_batalha(self.batalha_id, 'fugir')
        )
        self.btn_run.grid(row=1, column=1, padx=5, pady=5)
>>>>>>> Stashed changes

        self.atualizar_interface(batalha_info)
        self.after(50, self._redesenhar_imagem_fundo)

    # --- CORREÇÃO DO LOOP INFINITO (TRAVAMENTO) ---
    def _redesenhar_imagem_fundo(self, event=None):
        if not self.pil_bg_image:
            return
        
        width = self.status_frame.winfo_width()
        height = self.status_frame.winfo_height()

        # Se o tamanho for inválido ou o mesmo de antes, não faça nada
        if width <= 1 or height <= 1:
            return
        if width == self._last_bg_width and height == self._last_bg_height:
            return

        # Armazena o novo tamanho e só então redesenha
        self._last_bg_width = width
        self._last_bg_height = height
        
        self.bg_image_resized = ctk.CTkImage(self.pil_bg_image, size=(width, height))
        self.bg_image_label.configure(image=self.bg_image_resized)
    # --- FIM DA CORREÇÃO ---

    def atualizar_interface(self, batalha_info):
        pc_treinador = self.controller.get_treinador_pc()
        equipe_treinador = self.controller.get_treinador_equipe()

        pokemon_em_campo = next((p for p in equipe_treinador if p['id_captura'] == batalha_info['pokemon_em_campo_id_captura']), None)
        
        oponente = batalha_info['oponente']

        self.label_oponente_nome.config(text=f"{oponente['nome']} (Nv.{oponente['nivel']})")
        self.label_oponente_hp.config(text=f"HP: {oponente['hp_atual']} / {oponente['hp_max']}")
        
        if pokemon_em_campo:
            self.label_jogador_nome.config(text=f"{pokemon_em_campo['nome']} (Nv.{pokemon_em_campo['nivel']})")
            self.label_jogador_hp.config(text=f"HP: {pokemon_em_campo['hp']} / {pokemon_em_campo['hp_max']}")
            xp_atual = pokemon_em_campo.get('xp_atual', 0)
            xp_para_upar = pokemon_em_campo.get('xp_para_upar', 1) # Evita divisão por zero
            self.label_jogador_xp.config(text=f"XP: {xp_atual} / {xp_para_upar}")
        else:
            self.label_jogador_nome.config(text="Erro!")
            self.label_jogador_hp.config(text="HP: ?? / ??")
            
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("1.0", "\n".join(batalha_info['log_batalha']))
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)
        if 'resultado_final' in batalha_info:
<<<<<<< Updated upstream
            for child in self.botoes_frame.winfo_children(): 
                child.config(state="disabled")
=======
            for child in self.botoes_frame.winfo_children():
                child.configure(state="disabled")
>>>>>>> Stashed changes
