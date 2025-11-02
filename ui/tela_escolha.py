import customtkinter as ctk
from ui.ctk_messagebox import CTkMessageBox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TelaEscolha(ctk.CTkFrame):
    def __init__(self, master, controller, iniciais):
        super().__init__(master)
        self.controller = controller

        # TÍTULOS NO TOPO
        frame_titulos = ctk.CTkFrame(self, fg_color="#23272e", corner_radius=10)
        frame_titulos.pack(side="top", fill="x", pady=(20, 10), padx=16)
        ctk.CTkLabel(frame_titulos, text=f"Bem-vindo, {self.controller.get_treinador_nome()}!", font=("Arial", 20, "bold"), text_color="#FFD369").pack()
        ctk.CTkLabel(frame_titulos, text="Escolha seu companheiro de jornada:", font=("Arial", 16), text_color="#00adb5").pack(pady=(0, 20))

        # ÁREA DE ROLAGEM
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=12, pady=4)
        canvas = ctk.CTkCanvas(main_frame, bg="#23272e", highlightthickness=0, bd=0)
        scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="transparent")

        scroll_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        def frame_config(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", frame_config)
        def canvas_resize(event):
            canvas.itemconfig(scroll_id, width=event.width)
        canvas.bind("<Configure>", canvas_resize)

        # GRID DE INICIAIS
        row = col = 0
        for pokemon in iniciais:
            card = self.criar_card_pokemon(scrollable_frame, pokemon)
            card.grid(row=row, column=col, padx=(30,15), pady=15)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def criar_card_pokemon(self, parent, pokemon):
        nome_pokemon = pokemon['nome']
        tipos_pokemon = pokemon.get('tipagem', [])
        tipo_texto = tipos_pokemon[0] if tipos_pokemon else "Desconhecido"

        card_frame = ctk.CTkFrame(parent, fg_color="#393e46", corner_radius=16)
        placeholder_imagem = ctk.CTkLabel(card_frame, text="Imagem aqui", fg_color="#EEEEEE", width=110, height=60)
        placeholder_imagem.pack(padx=10, pady=(10, 5))
        nome_label = ctk.CTkLabel(card_frame, text=nome_pokemon, font=("Arial", 14, "bold"), text_color="#FFD369")
        nome_label.pack()
        tipo_label = ctk.CTkLabel(card_frame, text=tipo_texto, font=("Arial", 10, "italic"), text_color="#00adb5")
        tipo_label.pack(pady=(0, 10))

        def acao_clique(e=None, p_nome=pokemon['nome']):
            if p_nome and len(p_nome.strip()) > 0:
                self.controller.handle_escolher_inicial(p_nome)
            else:
                CTkMessageBox(self, "Aviso", "Pokémon inválido!", icon="warning")

        for widget in (card_frame, placeholder_imagem, nome_label, tipo_label):
            widget.bind("<Button-1>", acao_clique)
        return card_frame
