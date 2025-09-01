
import sys
import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Level import Level
from code.Menu import Menu



class Game:
    def __init__(self):
        pygame.init()
        
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Space Explorer")
        
        try:
            icon = pygame.Surface((32, 32))
            icon.fill((0, 0, 255))
            pygame.display.set_icon(icon)
        except:
            pass

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:
                self.start_new_game(menu_return)
            elif menu_return == MENU_OPTION[1] or menu_return is None:
                self.quit_game()
            else:
                continue

    def start_new_game(self, game_mode: str):
        player_score = [0]
        
        level = Level(self.window, 'Level1', game_mode, player_score)
        level_result = level.run(player_score)
        
        if level_result:
            self.show_victory_screen(player_score)
        else:
            self.show_game_over_screen("Missão falhou!")



    def show_victory_screen(self, player_scores: list):
        victory_time = 5000
        start_time = pygame.time.get_ticks()
        
        font_title = pygame.font.Font(None, 64)
        font_score = pygame.font.Font(None, 36)
        
        while pygame.time.get_ticks() - start_time < victory_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    return  # Pular tela de vitória
            
            self.window.fill((0, 50, 0))
            self.draw_stars(100)
            
            title_text = font_title.render("MISSÃO COMPLETA!", True, (0, 255, 0))
            title_rect = title_text.get_rect(center=(WIN_WIDTH // 2, 150))
            self.window.blit(title_text, title_rect)
            
            y_offset = 250
            
            congrats_text = font_score.render("Vitória!", True, (255, 255, 255))
            congrats_rect = congrats_text.get_rect(center=(WIN_WIDTH // 2, y_offset + 40))
            self.window.blit(congrats_text, congrats_rect)
            
            skip_text = pygame.font.Font(None, 24).render("Pressione qualquer tecla para continuar", True, (200, 200, 200))
            skip_rect = skip_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 40))
            self.window.blit(skip_text, skip_rect)
            
            pygame.display.flip()
            pygame.time.wait(16)

    def show_game_over_screen(self, message: str):
        game_over_time = 3000
        start_time = pygame.time.get_ticks()
        
        font_title = pygame.font.Font(None, 64)
        font_message = pygame.font.Font(None, 32)
        
        while pygame.time.get_ticks() - start_time < game_over_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    return  # Pular tela de game over
            
            self.window.fill((50, 0, 0))
            
            title_text = font_title.render("GAME OVER", True, (255, 0, 0))
            title_rect = title_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50))
            self.window.blit(title_text, title_rect)
            
            message_text = font_message.render(message, True, (255, 255, 255))
            message_rect = message_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 20))
            self.window.blit(message_text, message_rect)
            
            retry_text = font_message.render("Tente novamente!", True, (255, 255, 0))
            retry_rect = retry_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 80))
            self.window.blit(retry_text, retry_rect)
            
            skip_text = pygame.font.Font(None, 24).render("Pressione qualquer tecla para continuar", True, (200, 200, 200))
            skip_rect = skip_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 40))
            self.window.blit(skip_text, skip_rect)
            
            pygame.display.flip()
            pygame.time.wait(16)

    def draw_stars(self, count: int):
        import random
        random.seed(pygame.time.get_ticks() // 1000)
        
        for _ in range(count):
            x = random.randint(0, WIN_WIDTH)
            y = random.randint(0, WIN_HEIGHT)
            brightness = random.randint(100, 255)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.window, color, (x, y), random.choice([1, 1, 2]))

    def quit_game(self):
        pygame.quit()
        sys.exit()
