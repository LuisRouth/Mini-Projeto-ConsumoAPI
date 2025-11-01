# Mini Projeto de Jogo Pokémon com API

Este projeto é uma implementação de um RPG simples inspirado em Pokémon, desenvolvido como parte do "Mini-Projeto Consumo de APIs". Ele consiste em um backend (servidor) construído com FastAPI que gerencia toda a lógica do jogo, e um frontend (cliente) com interface gráfica construído com Tkinter que consome essa API.

## Funcionalidades Implementadas

- **Criação de Treinador**: Comece uma nova jornada criando seu próprio treinador.
- **Escolha de Inicial**: Selecione um dos 15 Pokémon iniciais de diferentes gerações.
- **Sistema de Áreas**: Explore 4 áreas distintas, cada uma com diferentes Pokémon, níveis e raridades. A progressão entre as áreas é bloqueada, requerendo vitórias em ginásios (funcionalidade futura).
- **Encontro de Pokémon**: Encontre Pokémon selvagens aleatoriamente ao explorar uma área.
- **Sistema de Batalha**:
  - Batalhas por turnos (atacar, capturar, fugir).
  - **Lógica de Tipos**: Efetividade de ataques (Super Efetivo, Não Muito Efetivo, Sem Efeito) baseada em uma tabela de tipos.
  - **Sistema de Experiência (XP)**: Pokémon da equipe ganham XP ao derrotar oponentes.
  - **Evolução por Nível**: Pokémon evoluem automaticamente ao atingirem o nível necessário.
- **Sistema de Captura**: A chance de captura aumenta conforme a vida do Pokémon selvagem diminui.
- **Equipe e PC**: Gerenciamento de uma equipe de até 6 Pokémon. Pokémon capturados com a equipe cheia são enviados automaticamente para o PC.
- **Centro Pokémon**: Funcionalidade de curar todos os Pokémon da equipe e do PC.

## Estrutura do Projeto

- **/server/app/**: Contém toda a lógica do backend da API.
  - `main.py`: Ponto de entrada da API FastAPI.
  - `/routers/`: Define os endpoints da API (treinador, mundo, batalha).
  - `crud.py`: Funções que manipulam o "banco de dados" (`gamestate.json`).
  - `type_logic.py`: Módulo com a lógica de efetividade de tipos.
  - `gamestate.json`: Arquivo que funciona como o save do jogo.
- **/ui/**: Contém os arquivos da interface gráfica do cliente, construída com Tkinter.
- `desktop_app.py`: Ponto de entrada principal do projeto. Inicia tanto o backend em uma thread separada quanto o frontend.

## Tecnologias Utilizadas

- **Backend**: Python, FastAPI
- **Frontend**: Python, Tkinter
- **Comunicação**: Requests
- **Servidor**: Uvicorn

## Como Executar o Projeto

Este projeto foi desenhado para ser executado com um único comando, simplificando a inicialização.

### Pré-requisitos

- Python 3.10 ou superior.

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd [NOME_DO_SEU_PROJETO]
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
 ```
Para sair do jogo, basta fechar a janela. A tecla Esc também remove o modo de tela cheia.