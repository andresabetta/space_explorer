#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION, C_WHITE, C_YELLOW, C_ORANGE
from code.Assets import load_optional


class Menu:
    def __init__(self, window):
        self.window = window
        self.background_color = (15, 15, 50)  # Azul escuro espacial
        self.selected_option = 0
        self.clock = pygame.time.Clock()
        
        # Configurações visuais
        self.title_font = pygame.font.Font(None, 64)
        self.option_font = pygame.font.Font(None, 36)
        self.subtitle_font = pygame.font.Font(None, 24)
        
        # Fundo de imagem opcional
        self.menu_bg = load_optional('MenuBg.png', (WIN_WIDTH, WIN_HEIGHT))
        
        # Animações
        self.star_particles = []
        self.create_star_particles()

    def create_star_particles(self):
        """Cria partículas de estrelas para o fundo"""
        import random
        
        for _ in range(100):
            x = random.randint(0, WIN_WIDTH)
            y = random.randint(0, WIN_HEIGHT)
            speed = random.uniform(0.5, 2.0)
            brightness = random.randint(100, 255)
            
            self.star_particles.append({
                'x': x,
                'y': y,
                'speed': speed,
                'brightness': brightness
            })

    def update_star_particles(self):
        """Atualiza as partículas de estrelas"""
        import random
        
        for star in self.star_particles:
            star['x'] -= star['speed']
            
            # Reset quando sai da tela
            if star['x'] < 0:
                star['x'] = WIN_WIDTH
                star['y'] = random.randint(0, WIN_HEIGHT)

    def draw_star_particles(self):
        """Desenha as partículas de estrelas"""
        for star in self.star_particles:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(self.window, color, 
                             (int(star['x']), int(star['y'])), 1)

    def run(self):
        """Loop principal do menu"""
        running = True
        
        while running:
            # Processar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return MENU_OPTION[self.selected_option]
                    elif event.key == pygame.K_ESCAPE:
                        return MENU_OPTION[4]  # SAIR

            # Atualizar animações
            self.update_star_particles()
            
            # Desenhar tudo
            self.draw_menu()
            
            self.clock.tick(60)
        
        return None

    def draw_menu(self):
        """Desenha o menu principal"""
        # Fundo
        if self.menu_bg is not None:
            self.window.blit(self.menu_bg, (0, 0))
        else:
            self.window.fill(self.background_color)
            self.draw_star_particles()
        
        # Título principal
        title_text = self.title_font.render("SPACE EXPLORER", True, C_YELLOW)
        title_rect = title_text.get_rect(center=(WIN_WIDTH // 2, 120))
        self.window.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = self.subtitle_font.render("Aventura Espacial de Plataforma", True, C_WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WIN_WIDTH // 2, 160))
        self.window.blit(subtitle_text, subtitle_rect)
        
        # Desenho decorativo (mantido se não houver background)
        if self.menu_bg is None:
            self.draw_spaceship(WIN_WIDTH // 2 - 100, 200)
        
        # Opções do menu
        start_y = 280
        for i, option in enumerate(MENU_OPTION):
            if i == self.selected_option:
                color = C_ORANGE
                indicator_text = self.option_font.render(">>>", True, C_ORANGE)
                self.window.blit(indicator_text, (WIN_WIDTH // 2 - 150, start_y + i * 50))
            else:
                color = C_WHITE
            
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(WIN_WIDTH // 2, start_y + i * 50))
            self.window.blit(option_text, option_rect)
        
        # Instruções
        instruction_text = self.subtitle_font.render(
            "Use SETAS para navegar, ENTER para selecionar", True, C_WHITE)
        instruction_rect = instruction_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 50))
        self.window.blit(instruction_text, instruction_rect)
        
        # Controles do jogo
        controls_text = self.subtitle_font.render(
            "P1: SETAS + CTRL | P2: WASD + CTRL", True, C_WHITE)
        controls_rect = controls_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 25))
        self.window.blit(controls_text, controls_rect)
        
        pygame.display.flip()

    def draw_spaceship(self, x, y):
        """Desenha uma nave espacial decorativa"""
        pygame.draw.ellipse(self.window, (200, 200, 200), (x, y, 200, 60))
        pygame.draw.ellipse(self.window, (100, 150, 255), (x + 60, y + 15, 80, 30))
        pygame.draw.rect(self.window, (255, 100, 100), (x - 20, y + 20, 30, 20))
        pygame.draw.rect(self.window, (255, 150, 0), (x - 15, y + 25, 20, 10))
        points_left = [(x + 20, y + 20), (x - 10, y), (x + 30, y + 10)]
        points_right = [(x + 170, y + 20), (x + 210, y), (x + 170, y + 10)]
        pygame.draw.polygon(self.window, (150, 150, 150), points_left)
        pygame.draw.polygon(self.window, (150, 150, 150), points_right)
