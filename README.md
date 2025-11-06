# Mini Projeto de Jogo Pokémon com API

Este projeto é uma implementação de um RPG simples inspirado em Pokémon, desenvolvido como parte do "Mini-Projeto Consumo de APIs". Ele consiste em um backend (servidor) construído com FastAPI que gerencia toda a lógica do jogo, e um frontend (cliente) com interface gráfica construído com CustomTkinter que consome essa API.

1.  **Backend (Servidor)**: Uma API robusta construída com **FastAPI** que gerencia toda a lógica do jogo, estado, batalhas e persistência de dados.
2.  **Frontend (Cliente)**: Uma interface gráfica moderna construída com **CustomTkinter** que consome a API do backend, proporcionando uma experiência de usuário interativa e modularizada em várias telas.

## Funcionalidades Implementadas

### ⚙️ Backend (API - FastAPI)

* **Gerenciamento de Treinador**: Criação de treinador e gerenciamento de equipe (6 Pokémon) e PC (30 slots).
* **Lógica de Jogo**:
    * **Sistema de Batalha (Selvagem)**: Lógica de turnos para atacar, capturar Pokémon selvagens ou fugir.
    * **Sistema de Batalha (Ginásio)**: Um endpoint separado e mais complexo para batalhas de ginásio contra a equipe completa de um líder, com lógica de progressão.
    * **Efetividade de Tipos**: Cálculo de multiplicador de dano, incluindo suporte para Pokémon com tipo duplo (dual-type).
    * **Progressão**: Sistema de XP, level-up e evolução automática ao atingir o nível necessário.
    * **Cálculo de Stats**: Stats (HP, Ataque) são calculados dinamicamente com base no nível, stats base e raridade do Pokémon.
* **Mundo e Exploração**:
    * Sistema de 4 áreas distintas, cada uma com suas próprias faixas de nível, raridades e taxas de encontro.
    * Progressão de área bloqueada pela vitória no ginásio anterior.
* **Persistência de Dados**: O estado do jogo (treinadores, Pokémon capturados, progresso) é salvo no arquivo `gamestate.json`, que atua como um banco de dados simples.
* **Gerenciamento de Pokémon**: Funções CRUD completas para adicionar, atualizar, mover (Equipe <-> PC) e **libertar (deletar)** Pokémon.

### 🖥️ Frontend (Cliente - CustomTkinter)

* **Arquitetura Multi-Telas**: A aplicação utiliza um controlador principal (`desktop_app.py`) para gerenciar e alternar entre diferentes "telas" (frames):
    * **`TelaLogin`**: Tela inicial para criação de um novo treinador.
    * **`TelaEscolha`**: Grid rolável para a seleção do Pokémon inicial.
    * **`TelaGeral`**: O "hub" principal do jogo.
        * Exibe a equipe atual do jogador.
        * Lista as áreas de exploração e ginásios, habilitando-os com base na progressão.
        * Painel de eventos dinâmico que exibe informações da área, encontros de Pokémon e **imagens de fundo diferentes para cada área**.
    * **`TelaBatalha` / `TelaBatalhaGinasio`**: Interfaces de batalha dedicadas que mostram HP, logs de combate e botões de ação (Lutar, Pokémon, Fugir, Capturar).
    * **`TelaPC`**: Janela modal (`Toplevel`) para gerenciamento completo da equipe e do PC, permitindo mover Pokémon entre os slots e **libertar Pokémon** com um botão de exclusão.
    * **`TelaTrocaPokemon`**: Janela modal usada durante batalhas para trocar o Pokémon ativo, desabilitando Pokémon desmaiados ou já em campo.
* **Componentes Reutilizáveis**:
    * **`PopupPadrao`**: Um sistema de popup modal padronizado para exibir mensagens de sucesso, erro e informação.
* **Performance**: Carregamento de imagens em *multi-threading* para não bloquear a interface principal (ex: imagens de fundo da `TelaGeral` e sprites na `TelaEscolha`).

## Tecnologias Utilizadas

-   **Backend**: Python, **FastAPI**
-   **Frontend**: Python, **CustomTkinter**, Pillow (PIL)
-   **Servidor**: Uvicorn
-   **Comunicação**: Requests (para o cliente consumir a API)
-   **Utilitários**: Multi-threading (para carregamento de assets)

## Como Executar o Projeto

Este projeto foi desenhado para ser executado com um único comando, simplificando a inicialização.

### Pré-requisitos

-   Python 3.10 ou superior.

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [[https://github.com/LuisRouth/Mini-Projeto-ConsumoAPI.git](https://github.com/LuisRouth/Mini-Projeto-ConsumoAPI.git)]
    cd [Mini-Projeto-ConsumoAPI]
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # No Windows
    python -m venv .venv
    .venv\Scripts\activate

    # No macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### Execução

Após a instalação, execute o seguinte comando no terminal. Ele irá resetar o save anterior, iniciar o servidor da API em segundo plano e abrir a janela do jogo.

```bash
python desktop_app.py