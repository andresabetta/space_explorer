# Aluno: Andre Sabetta - RU: 4739336

import pygame

from code.Entity import Entity
from code.Const import ENTITY_DAMAGE, ENTITY_SPEED


class Projectile(Entity):
    def __init__(self, name: str, position: tuple, size: tuple, direction: int, owner_tag: str):
        super().__init__(name, position, size)
        self.direction = 1 if direction >= 0 else -1
        self.owner_tag = owner_tag
        self.speed.x = ENTITY_SPEED.get(name, 8)
        self.damage = ENTITY_DAMAGE.get(name, 10)

    def update(self, platforms, targets):
        self.position.x += self.speed.x * self.direction
        self.update_rect()

        for platform in platforms:
            if self.check_collision(platform):
                return False
        for target in targets:
            if self.check_collision(target):
                target.take_damage(self.damage)
                return False
        return True

    def draw(self, surface):
        image = self.image if self.direction >= 0 else pygame.transform.flip(self.image, True, False)
        surface.blit(image, self.rect)
