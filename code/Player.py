
import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, SHOT_COOLDOWN
from code.Entity import Entity
from code.Projectile import Projectile


class Player(Entity):
    def __init__(self, name: str, position: tuple, size: tuple):
        super().__init__(name, position, size)
        self.keys_collected = 0
        self.collectibles_found = 0
        self.can_double_jump = False
        self.double_jump_used = False
        self.action_cooldown = 0
        self.invulnerable = False
        self.invulnerability_timer = 0
        self.shoot_cooldown_ms = 0

    def handle_input(self, keys, projectiles_list):

        self.velocity.x = 0
        self.velocity.y = 0
        if keys[PLAYER_KEY_LEFT[self.name]]:
            self.velocity.x = -self.speed.x
            self.facing_right = False
        if keys[PLAYER_KEY_RIGHT[self.name]]:
            self.velocity.x = self.speed.x
            self.facing_right = True
        if keys[PLAYER_KEY_UP[self.name]]:
            self.velocity.y = -self.speed.x
        if keys[PLAYER_KEY_DOWN[self.name]]:
            self.velocity.y = self.speed.x


        if keys[PLAYER_KEY_SHOOT[self.name]] and self.shoot_cooldown_ms <= 0:
            shot_name = 'Player1Shot'
            shot_pos = (self.rect.centerx + (14 if self.facing_right else -14), self.rect.centery - 4)
            direction = 1 if self.facing_right else -1
            projectile = Projectile(shot_name, shot_pos, (16, 8), direction, 'player')
            projectiles_list.append(projectile)
            self.shoot_cooldown_ms = SHOT_COOLDOWN['Player1']

    def update(self, platforms, enemies, collectibles, delta_ms):

        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.update_rect()
        

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT
        self.position.x = self.rect.x
        self.position.y = self.rect.y
        

        if not self.invulnerable:
            for enemy in enemies:
                if self.check_collision(enemy):
                    self.take_damage(enemy.damage)
                    self.invulnerable = True
                    self.invulnerability_timer = 1000

        

        if self.action_cooldown > 0:
            self.action_cooldown -= 1
        
        if self.invulnerable:
            self.invulnerability_timer -= delta_ms
            if self.invulnerability_timer <= 0:
                self.invulnerable = False
        
        if self.shoot_cooldown_ms > 0:
            self.shoot_cooldown_ms -= delta_ms
        
    def take_damage(self, damage: int):
        super().take_damage(damage)
        self.invulnerable = True
        self.invulnerability_timer = 1000

    def perform_action(self):
        pass

    def draw(self, surface):
        if self.invulnerable and (pygame.time.get_ticks() // 50) % 2 == 0:
            return
        image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
        surface.blit(image, self.rect)

    def reset_position(self, position: tuple):
        self.set_position(position)
        self.velocity = pygame.Vector2(0, 0)

    def get_stats(self):
        return {
            'health': self.health,
            'keys': self.keys_collected,
            'collectibles': self.collectibles_found,
            'score': self.score
        }
