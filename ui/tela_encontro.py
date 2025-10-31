import tkinter as tk

class TelaEncontro(tk.Toplevel):
    def __init__(self, master, controller, pokemon_encontrado):
        super().__init__(master)
        self.controller = controller
        self.pokemon = pokemon_encontrado
        
        self.title("Encontro!")
        self.geometry("400x200")

        self.transient(master)
        self.grab_set()

        label_texto = tk.Label(self, text=f"Um {pokemon_encontrado['nome']} selvagem apareceu! (Raridade: {pokemon_encontrado['raridade']})", font=("Arial", 14))
        label_texto.pack(pady=20)

        botoes_frame = tk.Frame(self)
        botoes_frame.pack(pady=10)

        btn_batalhar = tk.Button(botoes_frame, text="Batalhar", font=("Arial", 12), command=self.iniciar_batalha)
        btn_batalhar.pack(side="left", padx=10)
        
        btn_procurar_outro = tk.Button(botoes_frame, text="Procurar Outro", font=("Arial", 12), command=self.procurar_outro)
        btn_procurar_outro.pack(side="left", padx=10)
    
    def iniciar_batalha(self):
        self.destroy()
        self.controller.handle_iniciar_batalha(self.pokemon['nome'])

    def procurar_outro(self):
        self.destroy()
        self.controller.handle_procurar_pokemon()