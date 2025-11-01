# ui/tela_escolha.py - VERSÃO FINAL COM SCROLLBAR MAIS LARGA

import tkinter as tk

class TelaEscolha(tk.Frame):
    def __init__(self, master, controller, iniciais):
        super().__init__(master)
        self.controller = controller

        # --- TÍTULOS FIXOS NO TOPO ---
        frame_titulos = tk.Frame(self)
        frame_titulos.pack(side="top", fill="x", pady=(20, 10))
        
        tk.Label(frame_titulos, text=f"Bem-vindo, {self.controller.get_treinador_nome()}!", font=("Arial", 20)).pack()
        tk.Label(frame_titulos, text="Escolha seu companheiro de jornada:", font=("Arial", 16)).pack(pady=(0, 20))

        # --- CONTAINER PARA A ÁREA DE ROLAGEM ---
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_frame)
        
        # --- ALTERAÇÃO AQUI ---
        # Adicionado o parâmetro 'width=30' para deixar a barra de rolagem mais larga
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, width=30)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)

        # --- FRAME ROLÁVEL (ONDE OS CARDS REALMENTE FICAM) ---
        scrollable_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # --- GRID DE POKÉMON ---
        row = 0
        col = 0
        for pokemon in iniciais:
            card = self.criar_card_pokemon(scrollable_frame, pokemon)
            card.grid(row=row, column=col, padx=(30, 15), pady=15)
            
            col += 1
            if col > 2:
                col = 0
                row += 1

    def criar_card_pokemon(self, parent, pokemon):
        """Esta função não precisou de mudanças."""
        nome_pokemon = pokemon['nome']
        tipos_pokemon = pokemon.get('tipagem', [])
        tipo_texto = tipos_pokemon[0] if tipos_pokemon else "Desconhecido"

        card_frame = tk.Frame(parent, bd=2, relief="groove", cursor="hand2")

        placeholder_imagem = tk.Label(card_frame, text="", bg="white", width=20, height=8)
        placeholder_imagem.pack(padx=10, pady=(10, 5))

        nome_label = tk.Label(card_frame, text=nome_pokemon, font=("Arial", 14, "bold"))
        nome_label.pack()

        tipo_label = tk.Label(card_frame, text=tipo_texto, font=("Arial", 10, "italic"), fg="gray")
        tipo_label.pack(pady=(0, 10))

        acao_clique = lambda e, p_nome=pokemon['nome']: self.controller.handle_escolher_inicial(p_nome)
        
        card_frame.bind("<Button-1>", acao_clique)
        placeholder_imagem.bind("<Button-1>", acao_clique)
        nome_label.bind("<Button-1>", acao_clique)
        tipo_label.bind("<Button-1>", acao_clique)

        return card_frame