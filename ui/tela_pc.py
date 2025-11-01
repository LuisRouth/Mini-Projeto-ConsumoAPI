import tkinter as tk

class TelaPC(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("PC de Pokémon")
        self.attributes('-fullscreen', True)
        self.bind('<Escape>', self.fechar)
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        self.transient(master)
        self.grab_set()

        # --- ESTRUTURA VISUAL ---
        self.feedback_label = tk.Label(self, text="Selecione um Pokémon", font=("Arial", 14))
        self.feedback_label.pack(pady=10)

        self.pc_frame = tk.LabelFrame(self, text="Box: 1", font=("Arial", 16, "bold"), padx=10, pady=10)
        self.pc_frame.pack(padx=10)

        self.equipe_frame = tk.LabelFrame(self, text="Equipe", font=("Arial", 14, "bold"), padx=10, pady=10)
        self.equipe_frame.pack(padx=10, pady=20, fill="x")

        tk.Button(self, text="Fechar PC", font=("Arial", 14, "bold"), command=self.fechar).pack(pady=10)

        self.redesenhar_widgets()

    def redesenhar_widgets(self):
        # Limpa frames antes de redesenhar
        for widget in self.pc_frame.winfo_children(): widget.destroy()
        for widget in self.equipe_frame.winfo_children(): widget.destroy()
        
        # Desenha os slots do PC (estilo antigo e simples)
        pc_list = self.controller.get_treinador_pc()
        for i in range(30):
            pokemon = pc_list[i] if i < len(pc_list) and pc_list[i] is not None else None
            slot_widget = self.criar_slot_pc_simples(self.pc_frame, pokemon, "pc", i)
            slot_widget.grid(row=i//6, column=i%6, padx=5, pady=5)
            
        # Desenha os slots da Equipe (estilo novo e detalhado)
        equipe_list = self.controller.get_treinador_equipe()
        for i in range(6):
            pokemon = equipe_list[i] if i < len(equipe_list) else None
            slot_widget = self.criar_slot_equipe_detalhado(self.equipe_frame, pokemon, "equipe", i)
            slot_widget.pack(side="left", padx=5, expand=True)

    def criar_slot_pc_simples(self, parent, pokemon, lista_nome, index):
        """Cria o widget SIMPLES para os slots da Box do PC."""
        slot_frame = tk.Frame(parent, bd=1, relief="solid")
        
        img_placeholder = tk.Label(slot_frame, bg="white", width=10, height=4)
        img_placeholder.pack(padx=5, pady=5)
        
        nome = pokemon['nome'] if pokemon else "- Vazio -"
        cor = "black" if pokemon else "gray"
        nome_label = tk.Label(slot_frame, text=nome, font=("Arial", 9), fg=cor)
        nome_label.pack(padx=2, pady=(0, 5))
        
        clique_info = (lista_nome, index, pokemon)
        for widget in [slot_frame, img_placeholder, nome_label]:
            widget.bind("<Button-1>", lambda e, ci=clique_info: self.controller.handle_pc_click(ci))
        
        return slot_frame
        
    def criar_slot_equipe_detalhado(self, parent, pokemon, lista_nome, index):
        """Cria o widget DETALHADO apenas para os slots da Equipe."""
        slot_frame = tk.Frame(parent, bd=1, relief="solid")
        
        img_placeholder = tk.Label(slot_frame, bg="white", width=10, height=5)
        img_placeholder.pack(side="left", padx=5, pady=5)
        
        info_frame = tk.Frame(slot_frame)
        info_frame.pack(side="left", fill="x", expand=True, padx=5)

        if pokemon:
            pokedex_info = self.controller.get_pokedex_info(pokemon['pokedex_id'])
            tipagem = ", ".join(pokedex_info['tipagem']) if pokedex_info else "???"

            nome_label = tk.Label(info_frame, text=f"{pokemon['nome']} (Nv.{pokemon['nivel']})", font=("Arial", 9, "bold"), anchor="w")
            nome_label.pack(fill="x")
            
            tipo_label = tk.Label(info_frame, text=f"Tipo: {tipagem}", font=("Arial", 8), anchor="w")
            tipo_label.pack(fill="x")
            
            xp_label = tk.Label(info_frame, text=f"XP: {pokemon.get('xp_atual', 0)} / {pokemon.get('xp_para_upar', 1)}", font=("Arial", 8), anchor="w")
            xp_label.pack(fill="x")
        else:
            nome_label = tk.Label(info_frame, text="- Vazio -", font=("Arial", 9, "italic"), fg="gray")
            nome_label.pack(pady=10)

        clique_info = (lista_nome, index, pokemon)
        for widget in [slot_frame, img_placeholder, info_frame] + list(info_frame.winfo_children()):
            widget.bind("<Button-1>", lambda e, ci=clique_info: self.controller.handle_pc_click(ci))
            
        return slot_frame

    def fechar(self, event=None):
        if self.controller:
            self.controller.handle_fechar_pc()
            self.controller.pc_window = None
        self.destroy()