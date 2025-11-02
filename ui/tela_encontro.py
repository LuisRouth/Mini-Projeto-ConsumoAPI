import customtkinter as ctk
from ui.ctk_messagebox import CTkMessageBox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TelaEncontro(ctk.CTkToplevel):
    def __init__(self, master, controller, pokemon_encontrado):
        super().__init__(master)
        self.controller = controller
        self.pokemon = pokemon_encontrado

        self.title("Encontro!")
        self.geometry("400x200")
        self.transient(master)
        self.grab_set()

        self.label_texto = ctk.CTkLabel(
            self,
            text=f"Um {pokemon_encontrado['nome']} selvagem apareceu!\n(Raridade: {pokemon_encontrado['raridade']})",
            font=("Arial", 16, "bold"),
            text_color="#EEEEEE",
            fg_color="#222831",
            corner_radius=8,
            anchor="center",
            justify="center",
            width=350,
            height=70
        )
        self.label_texto.pack(pady=24, padx=20)

        self.botoes_frame = ctk.CTkFrame(self, fg_color="#393e46", corner_radius=12)
        self.botoes_frame.pack(pady=16)

        self.btn_batalhar = ctk.CTkButton(
            self.botoes_frame,
            text="Batalhar",
            font=("Arial", 14),
            corner_radius=14,
            fg_color="#00adb5",
            hover_color="#00515c",
            command=self.iniciar_batalha,
            width=120
        )
        self.btn_batalhar.pack(side="left", padx=18)

        self.btn_procurar_outro = ctk.CTkButton(
            self.botoes_frame,
            text="Procurar Outro",
            font=("Arial", 14),
            corner_radius=14,
            fg_color="#393e46",
            hover_color="#222831",
            command=self.procurar_outro,
            width=120
        )
        self.btn_procurar_outro.pack(side="left", padx=18)

    def iniciar_batalha(self):
        try:
            self.destroy()
            self.controller.handle_iniciar_batalha(self.pokemon['nome'])
        except Exception as e:
            CTkMessageBox(self, "Erro", f"Erro ao iniciar batalha: {e}", icon="error")

    def procurar_outro(self):
        try:
            self.destroy()
            self.controller.handle_procurar_pokemon()
        except Exception as e:
            CTkMessageBox(self, "Erro", f"Erro ao procurar outro Pokémon: {e}", icon="error")
