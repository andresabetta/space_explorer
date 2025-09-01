
import pygame


C_ORANGE = (255, 128, 0)
C_YELLOW = (255, 255, 128)
C_WHITE = (255, 255, 255)
C_GREEN = (0, 128, 0)
C_CYAN = (0, 128, 128)
C_BLUE = (0, 0, 255)
C_RED = (255, 0, 0)
C_PURPLE = (128, 0, 128)


EVENT_ENEMY = pygame.USEREVENT + 1
EVENT_TIMEOUT = pygame.USEREVENT + 2
EVENT_COLLECTIBLE = pygame.USEREVENT + 3


ENTITY_SPEED = {
    'Level1Bg0': 0,
    'Level1Bg1': 1,
    'Level1Bg2': 2,
    'Level1Bg3': 3,
    'Level1Bg4': 4,
    'Level1Bg5': 5,
    'Level1Bg6': 6,
    'Level2Bg0': 0,
    'Level2Bg1': 1,
    'Level2Bg2': 2,
    'Level2Bg3': 3,
    'Level2Bg4': 4,
    'Player1': 4,
    'Enemy1': 2,
    'Enemy2': 1,
    'Collectible': 0,
    'Platform': 0,
    'Door': 0,
    'Key': 0,
    'Player1Shot': 10,
    'Enemy1Shot': 7,
    'Enemy2Shot': 8,
}

# Vida das entidades
ENTITY_HEALTH = {
    'Level1Bg0': 999,
    'Level1Bg1': 999,
    'Level1Bg2': 999,
    'Level1Bg3': 999,
    'Level1Bg4': 999,
    'Level1Bg5': 999,
    'Level1Bg6': 999,
    'Level2Bg0': 999,
    'Level2Bg1': 999,
    'Level2Bg2': 999,
    'Level2Bg3': 999,
    'Level2Bg4': 999,
    'Player1': 200,
    'Enemy1': 50,
    'Enemy2': 60,
    'Collectible': 1,
    'Platform': 999,
    'Door': 999,
    'Key': 1,
    'Player1Shot': 1,
    'Enemy1Shot': 1,
    'Enemy2Shot': 1,
}

# Dano das entidades
ENTITY_DAMAGE = {
    'Level1Bg0': 0,
    'Level1Bg1': 0,
    'Level1Bg2': 0,
    'Level1Bg3': 0,
    'Level1Bg4': 0,
    'Level1Bg5': 0,
    'Level1Bg6': 0,
    'Level2Bg0': 0,
    'Level2Bg1': 0,
    'Level2Bg2': 0,
    'Level2Bg3': 0,
    'Level2Bg4': 0,
    'Player1': 0,
    'Enemy1': 30,
    'Enemy2': 40,
    'Collectible': 0,
    'Platform': 0,
    'Door': 0,
    'Key': 0,
    'Player1Shot': 35,
    'Enemy1Shot': 15,
    'Enemy2Shot': 20,
}

# Pontuação das entidades
ENTITY_SCORE = {
    'Level1Bg0': 0,
    'Level1Bg1': 0,
    'Level1Bg2': 0,
    'Level1Bg3': 0,
    'Level1Bg4': 0,
    'Level1Bg5': 0,
    'Level1Bg6': 0,
    'Level2Bg0': 0,
    'Level2Bg1': 0,
    'Level2Bg2': 0,
    'Level2Bg3': 0,
    'Level2Bg4': 0,
    'Player1': 0,
    'Enemy1': 150,
    'Enemy2': 200,
    'Collectible': 50,
    'Platform': 0,
    'Door': 0,
    'Key': 100,
}


MENU_OPTION = (
    'NOVO JOGO',
    'SAIR'
)

# Controles
PLAYER_KEY_UP = {'Player1': pygame.K_UP}
PLAYER_KEY_DOWN = {'Player1': pygame.K_DOWN}
PLAYER_KEY_LEFT = {'Player1': pygame.K_LEFT}
PLAYER_KEY_RIGHT = {'Player1': pygame.K_RIGHT}
PLAYER_KEY_SHOOT = {'Player1': pygame.K_SPACE}

SPAWN_TIME = 2500
TIMEOUT_STEP = 100
TIMEOUT_LEVEL = 60000


WIN_WIDTH = 800
WIN_HEIGHT = 600


SCORE_POS = {'Title': (WIN_WIDTH / 2, 50),
             'EnterName': (WIN_WIDTH / 2, 80),
             'Label': (WIN_WIDTH / 2, 90),
             'Name': (WIN_WIDTH / 2, 110),
             0: (WIN_WIDTH / 2, 110),
             1: (WIN_WIDTH / 2, 130),
             2: (WIN_WIDTH / 2, 150),
             3: (WIN_WIDTH / 2, 170),
             4: (WIN_WIDTH / 2, 190),
             5: (WIN_WIDTH / 2, 210),
             6: (WIN_WIDTH / 2, 230),
             7: (WIN_WIDTH / 2, 250),
             8: (WIN_WIDTH / 2, 270),
             9: (WIN_WIDTH / 2, 290),
             }

SHOT_COOLDOWN = {
    'Player1': 300,
    'Enemy2': 1200,
    'Enemy1': 900,
}
