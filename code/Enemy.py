#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import random

from code.Const import ENTITY_SPEED, SHOT_COOLDOWN
from code.Entity import Entity
from code.Projectile import Projectile


class Enemy(Entity):
    def __init__(self, name: str, position: tuple, size: tuple, patrol_points=None):
        super().__init__(name, position, size)
        self.patrol_points = patrol_points or []
        self.current_patrol_index = 0
        self.patrol_timer = 0
        self.patrol_delay = 60
        self.aggro_range = 150
        self.attack_cooldown = 0
        self.attack_delay = 45
        self.is_aggro = False
        self.target = None
        self.original_speed = self.speed.x
        self.shoot_cooldown_ms = 0
        
        if 'Enemy1' in name:
            self.behavior = 'patrol'
            self.attack_type = 'contact'
        elif 'Enemy2' in name:
            self.behavior = 'ambush'
            self.attack_type = 'ranged'
            self.projectile_cooldown = 0

    def update(self, players, platforms, projectiles_list=None, delta_ms=16):
        nearest_player = self.find_nearest_player(players)
        
        # Modo nave espacial: sempre perseguir o jogador mais próximo
        if nearest_player:
            self.target = nearest_player
            distance = self.distance_to(nearest_player)
            
            if distance < self.aggro_range:
                self.is_aggro = True
                self.speed.x = self.original_speed * 1.5
            else:
                self.is_aggro = False
                self.speed.x = self.original_speed
            
            # Orientar nave na direção do movimento
            self.facing_right = self.target.position.x > self.position.x
            
            # Movimento em direção ao jogador (modo nave espacial)
            self.space_combat_behavior(nearest_player)
        else:
            self.target = None
            self.is_aggro = False
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        if self.patrol_timer > 0:
            self.patrol_timer -= 1

        # Tiro à distância
        if self.attack_type == 'ranged' and self.target and projectiles_list is not None:
            if self.shoot_cooldown_ms <= 0:
                shot_name = 'Enemy2Shot'
                direction = 1 if self.target.position.x >= self.position.x else -1
                shot_pos = (self.rect.centerx + (12 if direction > 0 else -12), self.rect.centery - 2)
                projectile = Projectile(shot_name, shot_pos, (14, 6), direction, 'enemy')
                projectiles_list.append(projectile)
                self.shoot_cooldown_ms = SHOT_COOLDOWN['Enemy2']
            else:
                self.shoot_cooldown_ms -= delta_ms

    def patrol_behavior(self, platforms):
        if not self.patrol_points:
            if self.patrol_timer <= 0:
                self.velocity.x = -self.velocity.x if self.velocity.x != 0 else self.speed.x
                self.patrol_timer = self.patrol_delay
        else:
            if self.patrol_timer <= 0:
                target_point = self.patrol_points[self.current_patrol_index]
                direction = pygame.Vector2(target_point) - self.position
                
                if direction.length() < 10:
                    self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
                    self.patrol_timer = self.patrol_delay
                else:
                    direction = direction.normalize()
                    self.velocity.x = direction.x * self.speed.x
        
        self.position.x += self.velocity.x
        self.update_rect()
        
        for platform in platforms:
            if self.check_collision(platform):
                if self.velocity.x > 0:
                    self.rect.right = platform.rect.left
                    self.position.x = self.rect.x
                    self.velocity.x = -self.speed.x
                elif self.velocity.x < 0:
                    self.rect.left = platform.rect.right
                    self.position.x = self.rect.x
                    self.velocity.x = self.speed.x

    def space_combat_behavior(self, target):
        """Comportamento para modo nave espacial - sempre se move em direção ao jogador"""
        if not target:
            return
            
        # Calcular direção para o jogador
        direction = pygame.Vector2(target.position) - self.position
        
        if direction.length() > 0:
            direction = direction.normalize()
            
            # Movimento em X e Y para modo nave espacial (velocidade bem reduzida)
            self.velocity.x = direction.x * self.speed.x * 0.4  # 40% da velocidade original
            self.velocity.y = direction.y * self.speed.x * 0.2  # Movimento vertical bem lento
            
            # Atualizar posição
            self.position.x += self.velocity.x
            self.position.y += self.velocity.y
            self.update_rect()
            
            # Ataques baseados no tipo
            if self.attack_cooldown <= 0:
                if self.attack_type == 'ranged':
                    self.ranged_attack()
                elif self.attack_type == 'contact':
                    self.charge_attack()

    def ambush_behavior(self, players, platforms):
        """Comportamento original de emboscada (não usado no modo nave)"""
        if self.target and self.attack_cooldown <= 0:
            if self.attack_type == 'ranged':
                self.ranged_attack()
            elif self.attack_type == 'contact':
                self.charge_attack()
        
        if self.target:
            direction = pygame.Vector2(self.target.position) - self.position
            if abs(direction.x) > 20:
                self.velocity.x = direction.x / abs(direction.x) * self.speed.x
            else:
                self.velocity.x = 0
        
        self.position.x += self.velocity.x
        self.update_rect()

    def ranged_attack(self):
        if self.projectile_cooldown <= 0:
            self.projectile_cooldown = 90
            self.attack_cooldown = self.attack_delay

    def charge_attack(self):
        if self.target:
            direction = pygame.Vector2(self.target.position) - self.position
            self.velocity.x = direction.x / abs(direction.x) * self.speed.x * 2
            self.attack_cooldown = self.attack_delay

    def find_nearest_player(self, players):
        nearest = None
        min_distance = float('inf')
        
        for player in players:
            distance = self.distance_to(player)
            if distance < min_distance:
                min_distance = distance
                nearest = player
        
        return nearest

    def distance_to(self, entity):
        return (self.position - entity.position).length()

    def take_damage(self, damage: int):
        super().take_damage(damage)
        if self.target:
            direction = self.position - self.target.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.position += direction * 20
                self.update_rect()

    def draw(self, surface):
        image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
        surface.blit(image, self.rect)
