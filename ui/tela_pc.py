from .popup_padrao import PopupPadrao
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class TelaPC(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.title("PC de Pokémon")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        self.protocol("WM_DELETE_WINDOW", self.fechar)
        self.transient(master)
        self.grab_set()

        main_frame = ctk.CTkFrame(self, fg_color="#212121")
        main_frame.pack(fill="both", expand=True)

        # 1. Empacotar o Label no TOPO
        self.feedback_label = ctk.CTkLabel(main_frame, text="Selecione um Pokémon", font=("Arial", 18, "bold"), fg_color="#263238", text_color="white")
        self.feedback_label.pack(pady=20, fill="x", side="top") 

        # 2. Empacotar o Botão "Fechar PC" no FUNDO (primeiro)
        ctk.CTkButton(main_frame, text="Fechar PC", font=("Arial", 13, "bold"),
            fg_color="#c62828", text_color="white", hover_color="#ff5252",
            command=self.fechar).pack(pady=12, side="bottom") 

        # 3. Empacotar a "Equipe" no FUNDO (aparecerá acima do botão)
        equipe_box_frame = ctk.CTkFrame(main_frame, fg_color="#263238", border_color="#c62828", border_width=2, corner_radius=8)
        equipe_box_frame.pack(padx=24, pady=24, fill="x", side="bottom") 
        
        equipe_label = ctk.CTkLabel(equipe_box_frame, text="Sua Equipe", font=("Arial", 15, "bold"), text_color="white")
        equipe_label.pack(anchor="center", padx=10, pady=5)
        self.equipe_frame = ctk.CTkFrame(equipe_box_frame, fg_color="#263238")
        self.equipe_frame.pack(anchor="center", fill="x", padx=10, pady=8)

        # 4. Mudar o PC para ser um CTkScrollableFrame
        self.pc_frame = ctk.CTkScrollableFrame( 
            main_frame, 
            fg_color="#23272b", 
            border_color="#c62828", 
            border_width=2, 
            corner_radius=8
        )
        self.pc_frame.pack(padx=24, pady=(12,8), fill="both", expand=True) 

        self.redesenhar_widgets()

    def mostrar_aviso_padrao(self, mensagem, tipo="info", titulo="Aviso"):
        PopupPadrao(self, mensagem, titulo, tipo)

    def redesenhar_widgets(self):
        for widget in self.pc_frame.grid_slaves():
            widget.destroy()
        for widget in self.equipe_frame.grid_slaves():
            widget.destroy()

        # PC: 24 slots (4x6)
        pc_list = self.controller.get_treinador_pc() 
        self.pc_frame.grid_columnconfigure(tuple(range(6)), weight=1)
        self.pc_frame.grid_rowconfigure(tuple(range(4)), weight=1) 
        
        for i in range(30):
            pokemon = pc_list[i] if i < len(pc_list) and pc_list[i] is not None else None
            slot_widget = self.criar_slot_pc_simples(self.pc_frame, pokemon, "pc", i)
            slot_widget.grid(row=i//6, column=i%6, padx=12, pady=12, sticky="nsew")

        # Equipe: 6 slots pequenos, fontes menores
        equipe_list = self.controller.get_treinador_equipe()
        self.equipe_frame.grid_columnconfigure(tuple(range(6)), weight=1)
        for i in range(6):
            pokemon = equipe_list[i] if i < len(equipe_list) and equipe_list[i] else None
            slot_widget = self.criar_slot_equipe_detalhado(self.equipe_frame, pokemon, "equipe", i)
            slot_widget.grid(row=0, column=i, padx=10, pady=7, sticky="nsew")

    # --- NOVO RECURSO: Adicionado botão de exclusão ---
    def criar_slot_pc_simples(self, parent, pokemon, lista_nome, index):
        slot_frame = ctk.CTkFrame(parent, fg_color="#23272b", border_color="#c62828", border_width=2, corner_radius=7, width=120, height=70)
        
        placeholder = ctk.CTkLabel(slot_frame, text="🕹️", fg_color="#c62828", text_color="white", width=56, height=24, font=("Arial", 20))
        placeholder.pack(padx=8, pady=(10, 3))
        nome = pokemon['nome'] if (pokemon and isinstance(pokemon, dict) and "nome" in pokemon) else "- Vazio -"
        cor = "white" if pokemon else "gray"
        nome_label = ctk.CTkLabel(slot_frame, text=nome, font=("Arial", 12), text_color=cor, fg_color="#23272b")
        nome_label.pack(pady=(1, 8))
        
        clique_info = (lista_nome, index, pokemon)
        for widget in [slot_frame, placeholder, nome_label]:
            widget.bind("<Button-1>", lambda e, ci=clique_info: self.controller.handle_pc_click(ci))

        if pokemon:
            # Adiciona o botão de excluir
            btn_excluir = ctk.CTkButton(
                slot_frame, 
                text="X", 
                width=20, 
                height=20, 
                font=("Arial", 12, "bold"),
                fg_color="#424242", 
                text_color="white", 
                hover_color="#b71c1c",
                command=lambda p=pokemon: self.controller.handle_excluir_pokemon(p['id_captura'], p['nome'])
            )
            btn_excluir.place(relx=1.0, rely=0, anchor="ne", x=-5, y=5) # Posiciona no canto

        return slot_frame

    # --- NOVO RECURSO: Adicionado botão de exclusão ---
    def criar_slot_equipe_detalhado(self, parent, pokemon, lista_nome, index):
        slot_frame = ctk.CTkFrame(parent, fg_color="#263238", border_color="#c62828", border_width=2, corner_radius=9, width=145, height=70)
        
        placeholder = ctk.CTkLabel(slot_frame, text="🕹️", fg_color="#c62828", text_color="white", width=36, height=18, font=("Arial", 17))
        placeholder.pack(side="left", padx=6, pady=6)
        info_frame = ctk.CTkFrame(slot_frame, fg_color="#263238")
        info_frame.pack(side="left", fill="both", expand=True, padx=6, pady=7)
        
        if pokemon and isinstance(pokemon, dict) and "nome" in pokemon:
            pokedex_info = self.controller.get_pokedex_info(pokemon.get('pokedex_id', None))
            tipagem = ", ".join(pokedex_info['tipagem']) if pokedex_info and 'tipagem' in pokedex_info else "???"
            nome_label = ctk.CTkLabel(info_frame, text=f"{pokemon['nome']} (Nv.{pokemon['nivel']})", font=("Arial", 9, "bold"), text_color="white", anchor="w")
            nome_label.pack(fill="x", pady=2)
            tipo_label = ctk.CTkLabel(info_frame, text=f"Tipo: {tipagem}", font=("Arial", 8), text_color="#b0bec5", anchor="w")
            tipo_label.pack(fill="x", pady=1)
            xp_label = ctk.CTkLabel(info_frame, text=f"XP: {pokemon.get('xp_atual', 0)} / {pokemon.get('xp_para_upar', 1)}", font=("Arial", 8), text_color="#b0bec5", anchor="w")
            xp_label.pack(fill="x", pady=1)
            
            # Adiciona o botão de excluir
            btn_excluir = ctk.CTkButton(
                slot_frame, 
                text="X", 
                width=20, 
                height=20, 
                font=("Arial", 12, "bold"),
                fg_color="#424242", 
                text_color="white", 
                hover_color="#b71c1c",
                command=lambda p=pokemon: self.controller.handle_excluir_pokemon(p['id_captura'], p['nome'])
            )
            btn_excluir.place(relx=1.0, rely=0, anchor="ne", x=-5, y=5) # Posiciona no canto
            
        else:
            nome_label = ctk.CTkLabel(info_frame, text="- Vazio -", font=("Arial", 9, "italic"), text_color="gray")
            nome_label.pack(pady=13)
            
        clique_info = (lista_nome, index, pokemon)
        for widget in [slot_frame, placeholder, info_frame] + list(info_frame.winfo_children()):
            widget.bind("<Button-1>", lambda e, ci=clique_info: self.controller.handle_pc_click(ci))
        return slot_frame

    def fechar(self, event=None):
        if self.controller:
            self.controller.handle_fechar_pc()
            self.controller.pc_window = None
        self.destroy()