import tkinter as tk

class TelaGeral(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        
        # --- Frame Esquerdo: Ações do Treinador ---
        acoes_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        acoes_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        acoes_frame.pack_propagate(False) # Impede o frame de encolher

        tk.Label(acoes_frame, text=f"Ações de {self.controller.get_treinador_nome()}", font=("Arial", 20)).pack(pady=10)
        
        tk.Button(acoes_frame, text="Explorar a Área 1", font=("Arial", 16), command=self.controller.handle_procurar_pokemon).pack(pady=20, fill="x", padx=20)
        
        tk.Button(acoes_frame, text="Ver PC", font=("Arial", 16), command=lambda: self.controller.mostrar_aviso("O PC ainda não foi implementado!")).pack(pady=20, fill="x", padx=20)


        # --- Frame Direito: Eventos da Área ---
        self.eventos_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self.eventos_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.eventos_frame.pack_propagate(False)
        
        tk.Label(self.eventos_frame, text="Eventos da Área", font=("Arial", 20)).pack(pady=10)
        
        self.log_frame = tk.Frame(self.eventos_frame)
        self.log_frame.pack(pady=20, fill="both", expand=True)

        self.log_text_widget = tk.Text(self.log_frame, font=("Arial", 14), wrap="word", height=5, bd=0)
        self.log_text_widget.insert("1.0", "Comece a explorar para encontrar Pokémon!")
        self.log_text_widget.config(state="disabled")
        self.log_text_widget.pack(pady=20, padx=20)
        self.botoes_frame = tk.Frame(self.eventos_frame)
        self.botoes_frame.pack(side="bottom", pady=20)

        self.mostrar_acoes_padrao()


    def mostrar_encontro(self, pokemon_encontrado):
        """Atualiza a tela para mostrar um encontro com Pokémon."""
        
        texto_encontro = f"Um {pokemon_encontrado['nome']} selvagem apareceu!\n(Raridade: {pokemon_encontrado['raridade']})"
        self.log_text_widget.config(state="normal")
        self.log_text_widget.delete("1.0", "end")
        self.log_text_widget.insert("1.0", texto_encontro)
        self.log_text_widget.config(state="disabled")

        self.limpar_botoes_acoes()
        tk.Button(self.botoes_frame, text="Batalhar", font=("Arial", 12), command=lambda: self.controller.handle_iniciar_batalha(pokemon_encontrado['nome'])).pack(side="left", padx=5)
        tk.Button(self.botoes_frame, text="Procurar Outro", font=("Arial", 12), command=self.controller.handle_procurar_pokemon).pack(side="left", padx=5)
        tk.Button(self.botoes_frame, text="Voltar", font=("Arial", 12), command=self.mostrar_acoes_padrao).pack(side="left", padx=5)

    def mostrar_acoes_padrao(self):
        """Limpa o log e mostra apenas o botão do Ginásio."""
        self.log_text_widget.config(state="normal")
        self.log_text_widget.delete("1.0", "end")
        self.log_text_widget.insert("1.0", "O que você gostaria de fazer?")
        self.log_text_widget.config(state="disabled")

        self.limpar_botoes_acoes()
        tk.Button(self.botoes_frame, text="Ir para o Ginásio", font=("Arial", 14), command=lambda: self.controller.mostrar_aviso("Ginásio ainda em construção!")).pack(pady=10)

    def limpar_botoes_acoes(self):
        """Remove todos os widgets do frame de botões."""
        for widget in self.botoes_frame.winfo_children():
            widget.destroy()