#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.Entity import Entity


class Background(Entity):
    def __init__(self, name: str, position: tuple, size: tuple):
        super().__init__(name, position, size)
        self.original_position = pygame.Vector2(position)
        self.parallax_speed = self.speed.x
        
        # Para scroll horizontal infinito
        self.width = int(self.size.x)
        self.height = int(self.size.y)
        self.position.x = 0

    def update(self):
        """Atualiza o fundo com movimento paralaxe"""
        self.position.x -= self.parallax_speed
        
        # Loop quando sair totalmente da tela
        if self.position.x <= -self.width:
            self.position.x += self.width
        
        self.update_rect()

    def draw(self, surface):
        """Desenha o fundo usando a imagem em tiles para cobrir a tela"""
        x = int(self.position.x)
        # Desenhar duas cópias para cobrir a largura
        surface.blit(self.image, (x, 0))
        surface.blit(self.image, (x + self.width, 0))

    def reset(self):
        """Reseta o fundo para a posição inicial"""
        self.position = pygame.Vector2(self.original_position)
        self.update_rect()

    def set_speed(self, speed):
        """Define a velocidade do paralaxe"""
        self.parallax_speed = speed
