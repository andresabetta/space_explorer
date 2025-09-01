
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
        

        self.level_complete = False
        self.level_failed = False
        self.enemies_spawned = 0
        self.max_enemies_to_spawn = 12 if level_name == 'Level1' else 18
        self.max_concurrent_enemies = 4 if level_name == 'Level1' else 6
        self.time_remaining = TIMEOUT_LEVEL
        self.spawn_timer = 0
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)
        

        self.create_background()
        self.create_players()
        self.create_enemies()

    def create_background(self):
        for i in range(5):
            bg_name = f'{self.level_name}Bg{i}'
            bg = Background(bg_name, (0, 0), (WIN_WIDTH, WIN_HEIGHT))
            self.background_list.append(bg)



    def create_players(self):
        player1 = Player('Player1', (50, WIN_HEIGHT - 100), (59, 29))
        self.player_list.append(player1)



    def create_enemies(self):
        if self.level_name == 'Level1':
            enemy_configs = [
                (WIN_WIDTH + 50, 150, 'Enemy1'),
                (WIN_WIDTH + 100, 350, 'Enemy2'),
            ]
        else:
            enemy_configs = [
                (WIN_WIDTH + 50, 100, 'Enemy1'),
                (-50, 200, 'Enemy2'),
                (WIN_WIDTH + 100, 400, 'Enemy1'),
            ]
        
        for x, y, enemy_type in enemy_configs:
            if enemy_type == 'Enemy1':
                enemy_size = (86, 39)
            else:
                enemy_size = (96, 46)
            enemy = Enemy(enemy_type, (x, y), enemy_size)
            self.enemy_list.append(enemy)
            self.enemies_spawned += 1

    def run(self, player_score: list):
        running = True
        
        while running:
            delta_ms = self.clock.tick(60)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                elif event.type == EVENT_ENEMY:
                    self.spawn_enemy()
                
                elif event.type == EVENT_TIMEOUT:
                    self.time_remaining -= TIMEOUT_STEP
                    if self.time_remaining <= 0:
                        self.level_failed = True
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False


            keys = pygame.key.get_pressed()
            for player in self.player_list:
                player.handle_input(keys, self.projectile_list)

            self.spawn_timer += delta_ms
            if (len(self.enemy_list) < 1 and 
                self.enemies_spawned < self.max_enemies_to_spawn and 
                self.spawn_timer > 3000):
                self.spawn_enemy()
                self.spawn_timer = 0
            self.update_entities(delta_ms)
            self.check_level_conditions()
            self.draw_all()
            if self.level_complete:
                self.update_score(player_score)
                return True
            elif self.level_failed:
                return False
        
        return False

    def update_entities(self, delta_ms: int):
        for bg in self.background_list:
            bg.update()
        for player in self.player_list[:]:
            player.update(self.platform_list, self.enemy_list, self.collectible_list, delta_ms)
            
            if not player.is_alive():
                self.level_failed = True
            
            if player.position.y > WIN_HEIGHT:
                player.reset_position((50, WIN_HEIGHT - 100))
                player.take_damage(30)
        

        for enemy in self.enemy_list[:]:
            enemy.update(self.player_list, self.platform_list, self.projectile_list, delta_ms)
            if not enemy.is_alive():
                nearest_player = self.find_nearest_player(enemy)
                if nearest_player:
                    self.add_score(nearest_player, enemy.score)
                self.enemy_list.remove(enemy)
        

        for projectile in self.projectile_list[:]:
            if projectile.owner_tag == 'player':
                targets = self.enemy_list
            else:
                targets = self.player_list
            alive = projectile.update(self.platform_list, targets)
            if (projectile.position.x < -50 or projectile.position.x > WIN_WIDTH + 50):
                alive = False
            if not alive:
                self.projectile_list.remove(projectile)

    def spawn_enemy(self):
        if (len(self.enemy_list) < self.max_concurrent_enemies and 
            self.enemies_spawned < self.max_enemies_to_spawn and 
            self.player_list):
            
            player = self.player_list[0]
            player_center_x = player.rect.centerx
            
            spawn_sides = []
            if player_center_x < WIN_WIDTH * 0.7:
                spawn_sides = [(WIN_WIDTH + 50, 'right'), (WIN_WIDTH + 100, 'right')]
            if player_center_x > WIN_WIDTH * 0.3:
                spawn_sides.extend([(-50, 'left'), (-100, 'left')])
            
            if not spawn_sides:
                spawn_sides = [(WIN_WIDTH + 50, 'right'), (-50, 'left')]
            
            spawn_x, side = random.choice(spawn_sides)
            spawn_y = random.randint(50, WIN_HEIGHT - 100)
            enemy_type = random.choice(['Enemy1', 'Enemy2'])
            

            if enemy_type == 'Enemy1':
                enemy_size = (86, 39)
            else:
                enemy_size = (96, 46)
            new_enemy = Enemy(enemy_type, (spawn_x, spawn_y), enemy_size)
            self.enemy_list.append(new_enemy)
            self.enemies_spawned += 1
            


    def check_level_conditions(self):
        if not self.player_list:
            self.level_failed = True
            return
        

        if (self.enemies_spawned >= self.max_enemies_to_spawn and 
            len(self.enemy_list) == 0):
            self.level_complete = True

    def find_nearest_player(self, entity):
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
        player_index = 0
        self.player_score[player_index] += points

    def update_score(self, player_score):
        for i, player in enumerate(self.player_list):

            player_score[i] += player.health

    def draw_all(self):
        self.window.fill((0, 0, 0))
        
        for bg in self.background_list:
            bg.draw(self.window)
        
        for projectile in self.projectile_list:
            projectile.draw(self.window)
        
        for enemy in self.enemy_list:
            enemy.draw(self.window)
        
        for player in self.player_list:
            player.draw(self.window)
        self.draw_hud()
        
        pygame.display.flip()

    def draw_hud(self):
        font = pygame.font.Font(None, 24)
        
        time_text = font.render(f'Tempo: {self.time_remaining // 1000}s', True, C_WHITE)
        self.window.blit(time_text, (10, 10))
        
        y_offset = 40
        for i, player in enumerate(self.player_list):
            stats = player.get_stats()
            health_text = font.render(f'Vida: {stats["health"]}', True, C_WHITE)
            self.window.blit(health_text, (10, y_offset))
            y_offset += 40
        
        enemies_remaining = self.max_enemies_to_spawn - self.enemies_spawned + len(self.enemy_list)
        instruction = f"Destrua todos os inimigos! Restam: {enemies_remaining}"
        
        instruction_text = font.render(instruction, True, C_WHITE)
        text_rect = instruction_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 30))
        self.window.blit(instruction_text, text_rect)
