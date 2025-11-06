from .popup_padrao import PopupPadrao
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.configure(fg_color="#212121")

        self.nomevar = ctk.StringVar()

        frame = ctk.CTkFrame(self, fg_color="#23272b")
        frame.place(relx=0.33, rely=0.25, relwidth=0.34, relheight=0.40)

        ctk.CTkLabel(frame, text="Bem-vindo!", font=("Arial", 24, "bold"), text_color="white").pack(pady=(26,8))
        ctk.CTkLabel(frame, text="Digite seu nome de treinador:", font=("Arial", 16), text_color="white").pack(pady=(4,10))

        entry_nome = ctk.CTkEntry(frame, textvariable=self.nomevar, font=("Arial", 16), width=220)
        entry_nome.pack(pady=10)

        btn_iniciar = ctk.CTkButton(
            frame,
            text="Iniciar Jornada",
            font=("Arial", 16, "bold"),
            fg_color="#c62828",
            text_color="white",
            hover_color="#ff5252",
            command=self.iniciar_jornada
        )
        btn_iniciar.pack(pady=16)

    def mostrar_aviso(self, mensagem, tipo="info", titulo="Aviso"):
        PopupPadrao(self, mensagem, titulo=titulo, tipo=tipo)

    def iniciar_jornada(self):
        nome = self.nomevar.get()
        if nome:
            self.controller.handle_criar_treinador(nome)
        else:
            self.mostrar_aviso("Por favor, digite um nome.", tipo="erro")
