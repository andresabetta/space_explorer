#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Level import Level
from code.Menu import Menu



class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Inicializar mixer para som
        
        # Configurar janela
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Space Explorer - Aventura Espacial")
        
        # Tentar carregar ícone (opcional)
        try:
            icon = pygame.Surface((32, 32))
            icon.fill((0, 0, 255))
            pygame.display.set_icon(icon)
        except:
            pass

    def run(self):
        """Loop principal do jogo"""
        while True:
            # Mostrar menu principal
            menu = Menu(self.window)
            menu_return = menu.run()

            # Processar escolha do menu (2 opções)
            if menu_return == MENU_OPTION[0]:
                # Iniciar novo jogo 1P
                self.start_new_game(menu_return)
            elif menu_return == MENU_OPTION[1] or menu_return is None:
                # Sair do jogo
                self.quit_game()
            else:
                # Opção inválida, voltar ao menu
                continue

    def start_new_game(self, game_mode: str):
        """Inicia um novo jogo - apenas 1 nível"""
        player_score = [0]  # Apenas Player1
        
        # Apenas Nível 1
        level1 = Level(self.window, 'Level1', game_mode, player_score)
        level1_result = level1.run(player_score)
        
        if level1_result:
            # Jogo completo - mostrar tela de vitória
            self.show_victory_screen(player_score)
        else:
            # Falhou no nível 1
            self.show_game_over_screen("Você falhou no Nível 1!")



    def show_victory_screen(self, player_scores: list):
        """Mostra tela de vitória"""
        victory_time = 5000  # 5 segundos
        start_time = pygame.time.get_ticks()
        
        font_title = pygame.font.Font(None, 64)
        font_score = pygame.font.Font(None, 36)
        
        while pygame.time.get_ticks() - start_time < victory_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    return  # Pular tela de vitória
            
            # Fundo colorido
            self.window.fill((0, 50, 0))  # Verde escuro
            self.draw_stars(100)
            
            # Título
            title_text = font_title.render("MISSÃO COMPLETA!", True, (0, 255, 0))
            title_rect = title_text.get_rect(center=(WIN_WIDTH // 2, 150))
            self.window.blit(title_text, title_rect)
            
            # Mensagem de vitória
            y_offset = 250
            
            congrats_text = font_score.render("Você salvou a galáxia!", True, (255, 255, 255))
            congrats_rect = congrats_text.get_rect(center=(WIN_WIDTH // 2, y_offset + 40))
            self.window.blit(congrats_text, congrats_rect)
            
            skip_text = pygame.font.Font(None, 24).render("Pressione qualquer tecla para continuar", True, (200, 200, 200))
            skip_rect = skip_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 40))
            self.window.blit(skip_text, skip_rect)
            
            pygame.display.flip()
            pygame.time.wait(16)

    def show_game_over_screen(self, message: str):
        """Mostra tela de game over"""
        game_over_time = 3000  # 3 segundos
        start_time = pygame.time.get_ticks()
        
        font_title = pygame.font.Font(None, 64)
        font_message = pygame.font.Font(None, 32)
        
        while pygame.time.get_ticks() - start_time < game_over_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    return  # Pular tela de game over
            
            # Fundo vermelho escuro
            self.window.fill((50, 0, 0))
            
            # Título
            title_text = font_title.render("MISSÃO FALHOU", True, (255, 0, 0))
            title_rect = title_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50))
            self.window.blit(title_text, title_rect)
            
            # Mensagem
            message_text = font_message.render(message, True, (255, 255, 255))
            message_rect = message_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 20))
            self.window.blit(message_text, message_rect)
            
            # Instrução
            retry_text = font_message.render("Tente novamente!", True, (255, 255, 0))
            retry_rect = retry_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 80))
            self.window.blit(retry_text, retry_rect)
            
            skip_text = pygame.font.Font(None, 24).render("Pressione qualquer tecla para continuar", True, (200, 200, 200))
            skip_rect = skip_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 40))
            self.window.blit(skip_text, skip_rect)
            
            pygame.display.flip()
            pygame.time.wait(16)

    def draw_stars(self, count: int):
        """Desenha estrelas aleatórias no fundo"""
        import random
        
        # Usar seed baseado no tempo para consistência durante a animação
        random.seed(pygame.time.get_ticks() // 1000)
        
        for _ in range(count):
            x = random.randint(0, WIN_WIDTH)
            y = random.randint(0, WIN_HEIGHT)
            brightness = random.randint(100, 255)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.window, color, (x, y), random.choice([1, 1, 2]))

    def quit_game(self):
        """Finaliza o jogo"""
        pygame.quit()
        sys.exit()
