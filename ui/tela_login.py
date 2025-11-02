import customtkinter as ctk
from ui.ctk_messagebox import CTkMessageBox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.label = ctk.CTkLabel(
            self,
            text="Digite seu nome de Treinador",
            font=("Arial", 20),
            text_color="#FFFFFF",
            fg_color="#222831",
            corner_radius=10
        )
        self.label.pack(pady=30, padx=20)

        self.nomevar = ctk.StringVar()
        self.entrynome = ctk.CTkEntry(
            self,
            textvariable=self.nomevar,
            font=("Arial", 16),
            width=280,
            fg_color="#393e46",
            corner_radius=10
        )
        self.entrynome.pack(pady=10, padx=20)

        self.buttoncriar = ctk.CTkButton(
            self,
            text="Iniciar Jornada",
            font=("Arial", 16, "bold"),
            corner_radius=16,
            fg_color="#00adb5",
            hover_color="#393e46",
            command=self.iniciar_jornada
        )
        self.buttoncriar.pack(pady=30, padx=30)

    def iniciar_jornada(self):
        nome = self.nomevar.get()
        if nome and len(nome.strip()) > 0:
            self.controller.handle_criar_treinador(nome)
        else:
            CTkMessageBox(self, "Aviso", "Por favor, digite um nome.", icon="warning")
