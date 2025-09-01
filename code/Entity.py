#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.Const import ENTITY_SPEED, ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE
from code.Assets import load_image


class Entity:
    def __init__(self, name: str, position: tuple, size: tuple):
        self.name = name
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.speed = pygame.Vector2(ENTITY_SPEED.get(name, 0), 0)
        self.health = ENTITY_HEALTH.get(name, 1)
        self.damage = ENTITY_DAMAGE.get(name, 0)
        self.score = ENTITY_SCORE.get(name, 0)
        
        # Sprite e rect
        self.image = load_image(f"{name}.png", (int(size[0]), int(size[1])))
        self.rect = self.image.get_rect(topleft=(int(position[0]), int(position[1])))
        
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.facing_right = True

    def move(self, direction: pygame.Vector2):
        self.position += direction * self.speed.x
        self.update_rect()

    def update_rect(self):
        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

    def take_damage(self, damage: int):
        self.health -= damage
        return self.health <= 0

    def is_alive(self):
        return self.health > 0

    def get_rect(self):
        return self.rect

    def get_position(self):
        return self.position

    def set_position(self, position: tuple):
        self.position = pygame.Vector2(position)
        self.update_rect()

    def get_center(self):
        return (self.position.x + self.size.x // 2, 
                self.position.y + self.size.y // 2)

    def check_collision(self, other_entity):
        return self.rect.colliderect(other_entity.rect)

    def apply_gravity(self, gravity: float):
        self.velocity.y += gravity
        self.position.y += self.velocity.y
        self.update_rect()

    def jump(self, force: float):
        if self.on_ground:
            self.velocity.y = force
            self.on_ground = False

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image if self.facing_right else pygame.transform.flip(self.image, True, False), self.rect)
