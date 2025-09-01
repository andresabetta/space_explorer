# Principais Diferenças do Space Explorer

Este documento lista as principais mudanças realizadas para transformar o jogo original em algo completamente novo, evitando qualquer caracterização de plágio.

## Mudanças Fundamentais no Gameplay

### 1. Gênero Completamente Diferente
- **Original**: Jogo de tiro vertical (shooter)
- **Novo**: Jogo de plataforma com coleta e puzzles

### 2. Mecânicas de Movimento
- **Original**: Movimento livre em 8 direções + tiro
- **Novo**: Movimento de plataforma com gravidade, pulo simples e duplo

### 3. Objetivo do Jogo
- **Original**: Atirar em inimigos para ganhar pontos
- **Novo**: Coletar itens (gemas, chaves) para avançar de nível

### 4. Sistema de Combate
- **Original**: Tiro com projéteis
- **Novo**: Evitar inimigos ou derrotá-los por contato

## Novas Mecânicas Implementadas

### Física de Plataforma
- Sistema de gravidade realista
- Pulo duplo para maior mobilidade
- Colisões precisas com plataformas

### Tipos de Plataforma
- **Estáticas**: Plataformas normais
- **Móveis**: Se movem horizontalmente
- **Quebráveis**: Desmoronam após pisadas
- **Trampolim**: Impulsionam o jogador

### Sistema de Coleta
- **Gemas**: Pontuação básica (50 pts)
- **Chaves**: Necessárias para progressão (100 pts)
- **Corações**: Recuperam vida (50 pts)
- **Power-ups**: Efeitos temporários (75 pts)

### IA de Inimigos Avançada
- **Patrulheiros**: Seguem rotas predefinidas
- **Emboscadores**: Atacam quando jogador se aproxima
- **Sistema de Aggro**: Inimigos ficam mais agressivos próximos ao jogador

## Mudanças Visuais

### Interface
- **HUD Redesenhado**: Mostra vida, itens coletados, tempo
- **Menu Espacial**: Tema espacial com partículas de estrelas
- **Telas de Transição**: Entre níveis e vitória/derrota

### Arte Procedural
- **Fundo Paralaxe**: 5 camadas de fundo com efeitos visuais
- **Sprites Geométricos**: Formas coloridas ao invés de imagens
- **Efeitos de Partículas**: Estrelas, nebulosas, atmosfera

## Sistema de Progressão

### Níveis Únicos
- **Nível 1**: Introdução às mecânicas, plataformas simples
- **Nível 2**: Complexidade aumentada, mais inimigos

### Condições de Vitória
- Coletar número específico de gemas e chaves
- Sobreviver aos inimigos
- Completar dentro do tempo limite

### Sistema de Pontuação
- Pontos por coleta de itens
- Bônus por inimigos derrotados
- Bônus de vida restante
- Salvamento de melhores pontuações

## Modos de Jogo Expandidos

### Cooperativo
- Dois jogadores trabalham juntos
- Compartilham objetivo de coleta
- Pontuação combinada

### Competitivo
- Dois jogadores competem
- Pontuação individual
- Mesmos desafios, resultados separados

## Arquitetura de Código

### Novas Classes
- `Platform.py`: Sistema de plataformas com tipos diferentes
- `Collectible.py`: Itens coletáveis com animações
- Classes base reformuladas para suportar física de plataforma

### Sistemas Renovados
- **Física**: Gravidade, colisões, movimento inercial
- **Input**: Controles de plataforma ao invés de tiro
- **Colisão**: Sistema mais preciso para plataformas
- **Estado**: Gerenciamento de vida, itens, progressão

## Tema e Narrativa

### Ambientação
- **Original**: Montanha com inimigos genéricos
- **Novo**: Exploração espacial em mundos alienígenas

### Narrativa Implícita
- Explorador espacial em missão de coleta
- Mundos perigosos com criaturas hostis
- Objetivo de salvar a galáxia

## Conclusão

O **Space Explorer** mantém apenas a estrutura organizacional básica do projeto original, mas implementa:

1. **Gênero completamente diferente** (plataforma vs shooter)
2. **Mecânicas de jogo únicas** (coleta vs combate)
3. **Sistema de física próprio** (gravidade vs movimento livre)
4. **IA de inimigos avançada** (comportamentos vs movimento simples)
5. **Progressão baseada em objetivos** (coleta vs pontuação por tiro)
6. **Tema e arte distintos** (espaço vs montanha)

Estas mudanças fundamentais garantem que o jogo seja completamente original em termos de gameplay, mecânicas e experiência do jogador.
