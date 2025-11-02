import customtkinter as ctk
from ui.ctk_messagebox import CTkMessageBox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TelaTrocaPokemon(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.title("Escolha um Pokémon para lutar!")
        self.geometry("600x400")
        self.transient(master)
        self.grab_set()

        equipe_atual = self.controller.get_treinador_equipe()
        id_em_batalha = self.controller.batalha_atual['pokemon_em_campo_id_captura']

        self.party_frame = ctk.CTkFrame(self, fg_color="#393e46", corner_radius=12)
        self.party_frame.pack(pady=30, padx=24, expand=True, fill="both")

        for pokemon in equipe_atual:
            info_text = f"{pokemon['nome']} (Nv.{pokemon['nivel']})\nHP: {pokemon['hp']} / {pokemon['hp_max']}"
            def trocar(id_cap=pokemon['id_captura']):
                try:
                    self.controller.handle_trocar_pokemon(id_cap)
                except Exception as e:
                    CTkMessageBox(self, "Erro", f"Falha ao trocar Pokémon: {e}", icon="error")

            btn = ctk.CTkButton(
                self.party_frame,
                text=info_text,
                font=("Arial", 15, "bold"),
                corner_radius=16,
                fg_color="#00adb5" if pokemon['hp'] > 0 and pokemon['id_captura'] != id_em_batalha else "#444444",
                hover_color="#00515c" if pokemon['hp'] > 0 and pokemon['id_captura'] != id_em_batalha else "#222831",
                command=trocar,
                width=420,
            )
            btn.pack(pady=8, fill="x")
            if pokemon['hp'] <= 0:
                btn.configure(
                    state="disabled",
                    text=info_text + " - DESMAIADO",
                    fg_color="#23272e"
                )
            elif pokemon['id_captura'] == id_em_batalha:
                btn.configure(
                    state="disabled",
                    text=info_text + " - EM BATALHA",
                    fg_color="#353a3f"
                )

        self.btn_cancelar = ctk.CTkButton(
            self,
            text="Cancelar",
            font=("Arial", 15, "bold"),
            command=self.destroy,
            corner_radius=16,
            fg_color="#393e46",
            hover_color="#222831",
            width=200
        )
        self.btn_cancelar.pack(pady=20)
