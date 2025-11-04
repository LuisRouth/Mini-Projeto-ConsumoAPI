# ui/tela_troca_pokemon.py - VERSÃO FINAL E CORRIGIDA

import tkinter as tk

class TelaTrocaPokemon(tk.Toplevel):
    # --- A MUDANÇA ESTÁ AQUI NA ASSINATURA ---
    def __init__(self, master, controller, is_forced: bool = False):
        super().__init__(master)
        self.controller = controller
        
        self.title("Escolha um Pokémon para lutar!")
        self.geometry("600x400")
        self.transient(master)
        self.grab_set()

        equipe_atual = self.controller.get_treinador_equipe()
        id_em_batalha = self.controller.batalha_atual['pokemon_em_campo_id_captura']
        party_frame = tk.Frame(self)
        party_frame.pack(pady=20, padx=20, expand=True, fill="both")

        for pokemon in equipe_atual:
            if pokemon is None:
                continue
                
            info_text = f"{pokemon['nome']} (Nv.{pokemon['nivel']})\nHP: {pokemon['hp']} / {pokemon['hp_max']}"
            
            btn = tk.Button(
                party_frame, 
                text=info_text, 
                font=("Arial", 14), 
                command=lambda id_cap=pokemon['id_captura']: self.controller.handle_trocar_pokemon(id_cap)
            )
            btn.pack(pady=5, fill="x")
            if pokemon['hp'] <= 0:
                btn.config(state="disabled", text=info_text + " - DESMAIADO")
            if pokemon['id_captura'] == id_em_batalha:
                 btn.config(state="disabled", text=info_text + " - EM BATALHA")

        # --- E A MUDANÇA FINAL ESTÁ AQUI ---
        # O botão Cancelar só é criado se a troca NÃO for forçada
        if not is_forced:
            btn_cancelar = tk.Button(self, text="Cancelar", font=("Arial", 14), command=self.destroy)
            btn_cancelar.pack(pady=10)