import tkinter as tk

class TelaEscolha(tk.Frame):
    def __init__(self, master, controller, iniciais):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text=f"Bem-vindo, {self.controller.get_treinador_nome()}!", font=("Arial", 20)).pack(pady=20, padx=10)
        tk.Label(self, text="Escolha seu companheiro de jornada:", font=("Arial", 16)).pack(pady=20, padx=10)
        
        botoes_frame = tk.Frame(self)
        botoes_frame.pack(pady=10)

        row = 0
        col = 0
        for pokemon in iniciais:
            btn = tk.Button(
                botoes_frame, 
                text=pokemon['nome'], 
                font=("Arial", 14),
                width=15,
                command=lambda p_nome=pokemon['nome']: self.controller.handle_escolher_inicial(p_nome)
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
            
            col += 1
            if col > 2:
                col = 0
                row += 1 