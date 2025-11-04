from .popup_padrao import PopupPadrao
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class TelaEscolha(ctk.CTkFrame):
    def __init__(self, master, controller, iniciais):
        super().__init__(master)
        self.controller = controller
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.configure(fg_color="#212121") # cinza escuro

        # --- TÍTULOS NO TOPO ---
        frame_titulos = ctk.CTkFrame(self, fg_color="#212121")
        frame_titulos.place(relx=0, rely=0, relwidth=1, relheight=0.18)
        ctk.CTkLabel(
            frame_titulos,
            text=f"Bem-vindo, {self.controller.get_treinador_nome()}!",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(pady=(18, 5))
        ctk.CTkLabel(
            frame_titulos,
            text="Escolha seu companheiro de jornada:",
            font=("Arial", 18),
            text_color="#c62828" # vermelho escuro
        ).pack()

        # --- ÁREA DE ROLAGEM ---
        main_frame = ctk.CTkFrame(self, fg_color="#212121")
        main_frame.place(relx=0, rely=0.18, relwidth=1, relheight=0.82)

        canvas = ctk.CTkCanvas(main_frame, bg="#212121", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview, fg_color="#c62828")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        # FRAME ROLÁVEL
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="#212121")
        frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", on_frame_configure)

        # GRID DE POKÉMON
        row = 0
        col = 0
        COLUNAS = 5
        for pokemon in iniciais:
            card = self.criar_card_pokemon(scrollable_frame, pokemon)
            card.grid(row=row, column=col, padx=(20, 12), pady=15)
            col += 1
            if col >= COLUNAS:
                col = 0
                row += 1

    def mostrar_aviso_padrao(self, mensagem, tipo="info", titulo="Aviso"):
        PopupPadrao(self, mensagem, titulo, tipo)

    def criar_card_pokemon(self, parent, pokemon):
        nome_pokemon = pokemon['nome']
        tipos_pokemon = pokemon.get('tipagem', [])
        tipo_texto = tipos_pokemon[0] if tipos_pokemon else "Desconhecido"

        card_frame = ctk.CTkFrame(
            parent,
            border_width=2,
            border_color="#c62828",
            fg_color="#263238",
            cursor="hand2"
        )

        placeholder_imagem = ctk.CTkLabel(
            card_frame,
            text="🕹️",
            fg_color="#c62828",
            text_color="white",
            width=160,
            height=70,
            font=("Arial", 38)
        )
        placeholder_imagem.pack(padx=10, pady=(10, 5))

        nome_label = ctk.CTkLabel(
            card_frame,
            text=nome_pokemon,
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        nome_label.pack()

        tipo_label = ctk.CTkLabel(
            card_frame,
            text=tipo_texto,
            font=("Arial", 12, "italic"),
            text_color="#b0bec5"
        )
        tipo_label.pack(pady=(0, 10))

        def acao_clique(event=None, p_nome=nome_pokemon):
            try:
                self.controller.handle_escolher_inicial(p_nome)
            except Exception as exc:
                self.mostrar_aviso_padrao(f"Ocorreu um erro ao escolher o Pokémon: {exc}", tipo="erro")

        card_frame.bind("<Button-1>", acao_clique)
        placeholder_imagem.bind("<Button-1>", acao_clique)
        nome_label.bind("<Button-1>", acao_clique)
        tipo_label.bind("<Button-1>", acao_clique)
        return card_frame
