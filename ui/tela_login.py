import tkinter as tk

class TelaLogin(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        label = tk.Label(self, text="Digite seu nome de Treinador:", font=("Arial", 20))
        label.pack(pady=20)

        self.nome_var = tk.StringVar()
        entry_nome = tk.Entry(self, textvariable=self.nome_var, font=("Arial", 16), width=30)
        entry_nome.pack(pady=10)
        
        button_criar = tk.Button(self, text="Iniciar Jornada", font=("Arial", 16), command=self.iniciar_jornada)
        button_criar.pack(pady=20)

    def iniciar_jornada(self):
        nome = self.nome_var.get()
        if nome:
            self.controller.handle_criar_treinador(nome)
        else:
            self.controller.mostrar_aviso("Por favor, digite um nome.")