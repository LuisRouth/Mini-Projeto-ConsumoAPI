import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class TelaTrocaPokemon(ctk.CTkToplevel):
    def __init__(self, master, controller, is_forced=False, id_em_batalha=None):
        super().__init__(master)
        self.controller = controller
        self.title("Escolha um Pokémon para lutar!")
        self.geometry("600x420")
        self.transient(master)
        self.grab_set()

        equipe_atual = self.controller.get_treinador_equipe()

        party_frame = ctk.CTkFrame(self, fg_color="#212121")
        party_frame.pack(pady=24, padx=24, expand=True, fill="both")

        for pokemon in equipe_atual:
            if not pokemon:
                continue
            info_text = f"{pokemon['nome']} | Nv. {pokemon['nivel']} | HP: {pokemon['hp']}/{pokemon['hp_max']}"
            
            is_fainted = (pokemon['hp'] == 0)
            is_in_battle = (pokemon['id_captura'] == id_em_batalha)
            
            estado_cor = "#c62828" if is_fainted or is_in_battle else "#263238"
            hover_cor = "#ff5252" if is_fainted or is_in_battle else "#c62828"
            estado_txt = ""
            
            if is_in_battle:
                estado_txt = " - EM BATALHA"
            elif is_fainted:
                estado_txt = " - DESMAIADO"
                
            btn = ctk.CTkButton(
                party_frame,
                text=info_text + estado_txt,
                font=("Arial", 12),
                fg_color=estado_cor,
                text_color="white",
                hover_color=hover_cor,
                width=420,
                height=36,
                command=lambda idcap=pokemon['id_captura']: self.trocar_pokemon(idcap),
                state="disabled" if (is_fainted or is_in_battle) else "normal"
            )
            btn.pack(pady=6, fill="x")

        if not is_forced:
            btn_cancelar = ctk.CTkButton(self, text="Cancelar", font=("Arial", 12), fg_color="#263238", text_color="white", hover_color="#c62828", command=self.destroy)
            btn_cancelar.pack(pady=9)

    def trocar_pokemon(self, id_captura):
        self.destroy()
        self.controller.handle_trocar_pokemon(id_captura)