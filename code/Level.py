#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import random

from code.Const import (WIN_WIDTH, WIN_HEIGHT, EVENT_ENEMY, EVENT_TIMEOUT, 
                       TIMEOUT_STEP, TIMEOUT_LEVEL, SPAWN_TIME, C_WHITE)
from code.Background import Background
from code.Player import Player
from code.Enemy import Enemy
from code.Projectile import Projectile


class Level:
    def __init__(self, window, level_name: str, game_mode: str, player_score: list):
        self.window = window
        self.level_name = level_name
        self.game_mode = game_mode
        self.player_score = player_score
        self.clock = pygame.time.Clock()
        
        # Configurar entidades
        self.background_list = []
        self.platform_list = []
        self.player_list = []
        self.enemy_list = []
        self.collectible_list = []
        self.projectile_list = []
        
        # Configurações do nível
        self.level_complete = False
        self.level_failed = False
        self.enemies_spawned = 0
        self.max_enemies_to_spawn = 12 if level_name == 'Level1' else 18
        self.max_concurrent_enemies = 4 if level_name == 'Level1' else 6
        self.time_remaining = TIMEOUT_LEVEL
        self.spawn_timer = 0  # Timer adicional para forçar spawn
        
        # Eventos
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)
        
        # Inicializar nível
        self.create_background()
        self.create_players()
        self.create_enemies()

    def create_background(self):
        """Cria os layers de fundo com paralaxe"""
        for i in range(5):
            bg_name = f'{self.level_name}Bg{i}'
            bg = Background(bg_name, (0, 0), (WIN_WIDTH, WIN_HEIGHT))
            self.background_list.append(bg)



    def create_players(self):
        """Cria os jogadores baseado no modo de jogo"""
        player1 = Player('Player1', (50, WIN_HEIGHT - 100), (59, 29))  # Tamanho original da imagem
        self.player_list.append(player1)
        
        # 1 jogador apenas neste projeto



    def create_enemies(self):
        """Cria alguns inimigos iniciais no modo nave espacial"""
        # Spawn inicial menor no modo nave - a maioria virá via spawn automático
        if self.level_name == 'Level1':
            enemy_configs = [
                (WIN_WIDTH + 50, 150, 'Enemy1'),
                (WIN_WIDTH + 100, 350, 'Enemy2'),
            ]
        else:  # Level2
            enemy_configs = [
                (WIN_WIDTH + 50, 100, 'Enemy1'),
                (-50, 200, 'Enemy2'),
                (WIN_WIDTH + 100, 400, 'Enemy1'),
            ]
        
        for x, y, enemy_type in enemy_configs:
            # Tamanhos baseados nas imagens originais
            if enemy_type == 'Enemy1':
                enemy_size = (86, 39)
            else:  # Enemy2
                enemy_size = (96, 46)
            enemy = Enemy(enemy_type, (x, y), enemy_size)
            self.enemy_list.append(enemy)
            self.enemies_spawned += 1

    def run(self, player_score: list):
        """Loop principal do nível"""
        running = True
        
        while running:
            delta_ms = self.clock.tick(60)
            
            # Processar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                elif event.type == EVENT_ENEMY:
                    self.spawn_enemy()
                
                elif event.type == EVENT_TIMEOUT:
                    self.time_remaining -= TIMEOUT_STEP
                    if self.time_remaining <= 0:
                        self.level_failed = True  # Game over se o tempo acabar
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False

            # Processar input dos jogadores
            keys = pygame.key.get_pressed()
            for player in self.player_list:
                player.handle_input(keys, self.projectile_list)

            # Spawn forçado bem moderado
            self.spawn_timer += delta_ms
            if (len(self.enemy_list) < 1 and 
                self.enemies_spawned < self.max_enemies_to_spawn and 
                self.spawn_timer > 3000):  # Forçar spawn a cada 3s se nenhum inimigo
                self.spawn_enemy()
                self.spawn_timer = 0
            
            # Atualizar entidades
            self.update_entities(delta_ms)
            
            # Verificar condições de vitória/derrota
            self.check_level_conditions()
            
            # Desenhar tudo
            self.draw_all()
            
            # Verificar se o nível acabou
            if self.level_complete:
                self.update_score(player_score)
                return True
            elif self.level_failed:
                return False
        
        return False

    def update_entities(self, delta_ms: int):
        """Atualiza todas as entidades do jogo"""
        # Atualizar fundo
        for bg in self.background_list:
            bg.update()
        
        # Atualizar jogadores
        for player in self.player_list[:]:
            player.update(self.platform_list, self.enemy_list, self.collectible_list, delta_ms)
            
            if not player.is_alive():
                self.level_failed = True
            
            if player.position.y > WIN_HEIGHT:
                player.reset_position((50, WIN_HEIGHT - 100))
                player.take_damage(30)
        
        # Atualizar inimigos
        for enemy in self.enemy_list[:]:
            enemy.update(self.player_list, self.platform_list, self.projectile_list, delta_ms)
            if not enemy.is_alive():
                nearest_player = self.find_nearest_player(enemy)
                if nearest_player:
                    self.add_score(nearest_player, enemy.score)
                self.enemy_list.remove(enemy)
        
        # Atualizar projéteis
        for projectile in self.projectile_list[:]:
            if projectile.owner_tag == 'player':
                targets = self.enemy_list
            else:
                targets = self.player_list
            alive = projectile.update(self.platform_list, targets)
            # Remover se saiu da tela
            if (projectile.position.x < -50 or projectile.position.x > WIN_WIDTH + 50):
                alive = False
            if not alive:
                self.projectile_list.remove(projectile)
        
        # Coletáveis e plataformas removidos no modo nave

    def spawn_enemy(self):
        """Spawna um novo inimigo do lado oposto ao jogador"""
        if (len(self.enemy_list) < self.max_concurrent_enemies and 
            self.enemies_spawned < self.max_enemies_to_spawn and 
            self.player_list):
            
            player = self.player_list[0]
            player_center_x = player.rect.centerx
            
            # Spawn do lado oposto ao jogador com variação
            spawn_sides = []
            if player_center_x < WIN_WIDTH * 0.7:  # Se jogador está mais à esquerda
                spawn_sides = [(WIN_WIDTH + 50, 'right'), (WIN_WIDTH + 100, 'right')]
            if player_center_x > WIN_WIDTH * 0.3:  # Se jogador está mais à direita  
                spawn_sides.extend([(-50, 'left'), (-100, 'left')])
            
            if not spawn_sides:
                spawn_sides = [(WIN_WIDTH + 50, 'right'), (-50, 'left')]
            
            spawn_x, side = random.choice(spawn_sides)
            spawn_y = random.randint(50, WIN_HEIGHT - 100)
            enemy_type = random.choice(['Enemy1', 'Enemy2'])
            
            # Tamanhos baseados nas imagens originais
            if enemy_type == 'Enemy1':
                enemy_size = (86, 39)
            else:  # Enemy2
                enemy_size = (96, 46)
            new_enemy = Enemy(enemy_type, (spawn_x, spawn_y), enemy_size)
            self.enemy_list.append(new_enemy)
            self.enemies_spawned += 1
            


    def check_level_conditions(self):
        """Verifica condições de vitória e derrota"""
        if not self.player_list:
            self.level_failed = True
            return
        
        # Vitória: eliminar todos os inimigos spawned
        if (self.enemies_spawned >= self.max_enemies_to_spawn and 
            len(self.enemy_list) == 0):
            self.level_complete = True

    def find_nearest_player(self, entity):
        """Encontra o jogador mais próximo de uma entidade"""
        if not self.player_list:
            return None
        
        nearest = self.player_list[0]
        min_distance = (entity.position - nearest.position).length()
        
        for player in self.player_list[1:]:
            distance = (entity.position - player.position).length()
            if distance < min_distance:
                min_distance = distance
                nearest = player
        
        return nearest

    def add_score(self, player, points):
        """Adiciona pontos a um jogador"""
        player_index = 0
        self.player_score[player_index] += points

    def update_score(self, player_score):
        """Atualiza a pontuação final"""
        for i, player in enumerate(self.player_list):
            # Pontos apenas por inimigos destruídos (já adicionados) e bônus de vida restante
            player_score[i] += player.health

    def draw_all(self):
        """Desenha todos os elementos na tela"""
        # Limpar tela
        self.window.fill((0, 0, 0))
        
        # Desenhar fundo
        for bg in self.background_list:
            bg.draw(self.window)
        
        # Plataformas e coletáveis removidos no modo nave
        
        # Desenhar projéteis
        for projectile in self.projectile_list:
            projectile.draw(self.window)
        
        # Desenhar inimigos
        for enemy in self.enemy_list:
            enemy.draw(self.window)
        
        # Desenhar jogadores
        for player in self.player_list:
            player.draw(self.window)
        
        # Desenhar HUD
        self.draw_hud()
        
        pygame.display.flip()

    def draw_hud(self):
        """Desenha a interface do usuário"""
        font = pygame.font.Font(None, 24)
        
        # Tempo restante
        time_text = font.render(f'Tempo: {self.time_remaining // 1000}s', True, C_WHITE)
        self.window.blit(time_text, (10, 10))
        
        # Informações dos jogadores
        y_offset = 40
        for i, player in enumerate(self.player_list):
            stats = player.get_stats()
            
            # Vida
            health_text = font.render(f'P{i+1} Vida: {stats["health"]}', True, C_WHITE)
            self.window.blit(health_text, (10, y_offset))
            
            y_offset += 40
        
        # Instruções
        # Informações da missão
        enemies_remaining = self.max_enemies_to_spawn - self.enemies_spawned + len(self.enemy_list)
        instruction = f"Destrua todos os inimigos! Restam: {enemies_remaining}"
        
        instruction_text = font.render(instruction, True, C_WHITE)
        text_rect = instruction_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 30))
        self.window.blit(instruction_text, text_rect)
