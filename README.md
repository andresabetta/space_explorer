# Space Explorer

**Aluno:** Andre Sabetta - RU: 4739336  

Um jogo de combate espacial desenvolvido em Python com Pygame, onde você controla uma nave espacial enfrentando ondas de inimigos.

## Características do Jogo

### Mecânicas Principais
- **Combate Espacial**: Controle sua nave e atire em inimigos
- **Movimento Livre**: Voe em todas as direções no espaço
- **Inimigos Inteligentes**: Naves inimigas que perseguem e atacam
- **Sistema de Vida**: Tome dano e pisque quando atingido

### Controles
- **Setas**: Movimento da nave em 8 direções
- **Espaço**: Atirar
- **ESC**: Sair do jogo

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
- Destrua todas as naves inimigas para vencer
- Sobreviva aos ataques inimigos
- Use o espaço para atirar

### Dicas
- Mova-se constantemente para evitar projéteis
- Inimigos aparecem das bordas da tela
- Sua nave pisca quando toma dano
- Elimine todos os inimigos para completar o nível

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
    ├── Level.py        # Lógica do nível
    ├── Entity.py       # Classe base para entidades
    ├── Player.py       # Lógica da nave do jogador
    ├── Enemy.py        # IA das naves inimigas
    ├── Projectile.py   # Sistema de projéteis
    ├── Background.py   # Sistema de fundo
    └── Const.py        # Constantes do jogo
```

## Requisitos do Sistema

- Python 3.7 ou superior
- Pygame 2.1.0 ou superior
- 50MB de espaço livre
- Resolução mínima: 800x600

## Créditos

Jogo de combate espacial desenvolvido em Python com Pygame.
