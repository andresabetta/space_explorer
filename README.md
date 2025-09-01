# Space Explorer - Aventura Espacial de Plataforma

Um jogo de plataforma espacial desenvolvido em Python com Pygame, onde você controla um explorador espacial em busca de gemas e chaves em ambientes alienígenas perigosos.

## Características do Jogo

### Mecânicas Principais
- **Movimento de Plataforma**: Pule, corra e explore mundos espaciais
- **Sistema de Coleta**: Colete gemas, chaves e power-ups
- **Múltiplos Tipos de Plataforma**:
  - Estáticas (marrom)
  - Móveis (azul)
  - Quebráveis (laranja) 
  - Trampolim (verde)
- **Inimigos Inteligentes**: 
  - Patrulheiros que seguem rotas
  - Emboscadores que atacam quando você se aproxima
- **Física Realista**: Gravidade, pulo duplo e colisões precisas

### Modos de Jogo
1. **1 Jogador**: Aventura solo
2. **2 Jogadores Cooperativo**: Trabalhem juntos para completar os níveis
3. **2 Jogadores Competitivo**: Compitam por maior pontuação

### Controles
- **Jogador 1**: Setas do teclado + Ctrl direito
- **Jogador 2**: WASD + Ctrl esquerdo
- **ESC**: Pausar/Voltar ao menu

## Instalação

1. Certifique-se de ter Python 3.7+ instalado
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o jogo:
```bash
python main.py
```

## Como Jogar

### Objetivo
- Colete todas as gemas e chaves em cada nível
- Evite ou derrote os inimigos
- Complete os dois níveis para vencer

### Dicas
- Use o pulo duplo para alcançar plataformas altas
- Plataformas quebráveis desmoronam depois de um tempo
- Plataformas trampolim te impulsionam para cima
- Inimigos ficam mais agressivos quando você se aproxima
- Colete corações para recuperar vida
- Power-ups aumentam temporariamente sua velocidade

### Pontuação
- Gemas: 50 pontos cada
- Chaves: 100 pontos cada
- Power-ups: 75 pontos cada
- Inimigos derrotados: 150-200 pontos
- Bônus de vida restante no final

## Estrutura do Projeto

```
SpaceExplorer/
├── main.py              # Arquivo principal
├── requirements.txt     # Dependências
├── README.md           # Este arquivo
└── code/               # Código fonte
    ├── __init__.py     # Pacote Python
    ├── Game.py         # Classe principal do jogo
    ├── Menu.py         # Sistema de menus
    ├── Level.py        # Lógica dos níveis
    ├── Score.py        # Sistema de pontuação
    ├── Entity.py       # Classe base para entidades
    ├── Player.py       # Lógica do jogador
    ├── Enemy.py        # IA dos inimigos
    ├── Platform.py     # Sistema de plataformas
    ├── Collectible.py  # Itens coletáveis
    ├── Background.py   # Sistema de fundo paralaxe
    └── Const.py        # Constantes do jogo
```

## Requisitos do Sistema

- Python 3.7 ou superior
- Pygame 2.1.0 ou superior
- 50MB de espaço livre
- Resolução mínima: 800x600

## Créditos

Desenvolvido como projeto educacional baseado em conceitos de jogos de plataforma clássicos, com foco em mecânicas de exploração espacial e aventura cooperativa.
