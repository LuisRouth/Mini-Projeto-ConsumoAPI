import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class TelaEncontro(ctk.CTkToplevel):
    def __init__(self, master, controller, pokemon_encontrado):
        super().__init__(master)
        self.controller = controller
        self.pokemon = pokemon_encontrado
        self.title("Encontro!")
        self.geometry("450x200")
        self.transient(master)
        self.grab_set()

        # Mensagem com nome e raridade
        texto = f"Um {self.pokemon['nome']} selvagem apareceu!\nRaridade: {self.pokemon['raridade']}"
        label_texto = ctk.CTkLabel(self, text=texto, font=("Arial", 16, "bold"), text_color="white", fg_color="#23272b")
        label_texto.pack(pady=22, padx=10, fill="x")

        # Botões
        botoes_frame = ctk.CTkFrame(self, fg_color="#23272b")
        botoes_frame.pack(pady=15)
        btn_batalhar = ctk.CTkButton(botoes_frame, text="Batalhar", font=("Arial", 14), fg_color="#c62828", text_color="white", hover_color="#ff5252", width=100, command=self.iniciar_batalha)
        btn_batalhar.pack(side="left", padx=14)
        btn_procurar_outro = ctk.CTkButton(botoes_frame, text="Procurar Outro", font=("Arial", 14), fg_color="#263238", text_color="white", hover_color="#b71c1c", width=120, command=self.procurar_outro)
        btn_procurar_outro.pack(side="left", padx=14)

    def iniciar_batalha(self):
        self.destroy()
        self.controller.handle_iniciar_batalha(self.pokemon['nome'])

    def procurar_outro(self):
        self.destroy()
        self.controller.handle_procurar_pokemon()
