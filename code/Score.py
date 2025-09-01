#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import json
import os

from code.Const import WIN_WIDTH, WIN_HEIGHT, SCORE_POS, C_WHITE, C_YELLOW, C_GREEN


class Score:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.score_file = 'space_explorer_scores.json'
        
        # Carregar pontuações existentes
        self.high_scores = self.load_scores()

    def load_scores(self):
        """Carrega as pontuações do arquivo"""
        try:
            if os.path.exists(self.score_file):
                with open(self.score_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                return []
        except:
            return []

    def save_scores(self):
        """Salva as pontuações no arquivo"""
        try:
            with open(self.score_file, 'w', encoding='utf-8') as file:
                json.dump(self.high_scores, file, indent=2, ensure_ascii=False)
        except:
            pass

    def save(self, game_mode: str, player_scores: list):
        """Salva uma nova pontuação"""
        player_name = self.get_player_name(game_mode, player_scores)
        
        if player_name:
            # Calcular pontuação total
            total_score = sum(player_scores)
            
            # Criar entrada de pontuação
            score_entry = {
                'name': player_name,
                'score': total_score,
                'mode': game_mode,
                'individual_scores': player_scores.copy()
            }
            
            # Adicionar à lista
            self.high_scores.append(score_entry)
            
            # Ordenar por pontuação (maior primeiro)
            self.high_scores.sort(key=lambda x: x['score'], reverse=True)
            
            # Manter apenas top 10
            self.high_scores = self.high_scores[:10]
            
            # Salvar no arquivo
            self.save_scores()

    def get_player_name(self, game_mode: str, player_scores: list):
        """Obtém o nome do jogador para salvar a pontuação"""
        name = ""
        input_active = True
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if name.strip():
                            input_active = False
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 20 and event.unicode.isprintable():
                            name += event.unicode

            # Desenhar tela de entrada de nome
            self.draw_name_input_screen(game_mode, player_scores, name)
            self.clock.tick(60)
        
        return name.strip()

    def draw_name_input_screen(self, game_mode: str, player_scores: list, current_name: str):
        """Desenha a tela de entrada de nome"""
        self.window.fill((15, 15, 50))
        
        # Título
        title_text = self.font.render("PARABÉNS!", True, C_YELLOW)
        title_rect = title_text.get_rect(center=(WIN_WIDTH // 2, 100))
        self.window.blit(title_text, title_rect)
        
        # Pontuação
        total_score = sum(player_scores)
        score_text = self.font.render(f"Pontuação Total: {total_score}", True, C_GREEN)
        score_rect = score_text.get_rect(center=(WIN_WIDTH // 2, 150))
        self.window.blit(score_text, score_rect)
        
        # Modo de jogo
        mode_text = self.small_font.render(f"Modo: {game_mode}", True, C_WHITE)
        mode_rect = mode_text.get_rect(center=(WIN_WIDTH // 2, 180))
        self.window.blit(mode_text, mode_rect)
        
        # Pontuações individuais se houver múltiplos jogadores
        if len(player_scores) > 1:
            for i, score in enumerate(player_scores):
                player_text = self.small_font.render(f"Jogador {i+1}: {score}", True, C_WHITE)
                player_rect = player_text.get_rect(center=(WIN_WIDTH // 2, 210 + i * 25))
                self.window.blit(player_text, player_rect)
        
        # Prompt para nome
        prompt_text = self.font.render("Digite seu nome:", True, C_WHITE)
        prompt_rect = prompt_text.get_rect(center=(WIN_WIDTH // 2, 300))
        self.window.blit(prompt_text, prompt_rect)
        
        # Campo de entrada
        name_text = self.font.render(current_name + "_", True, C_YELLOW)
        name_rect = name_text.get_rect(center=(WIN_WIDTH // 2, 340))
        pygame.draw.rect(self.window, (50, 50, 50), 
                        (name_rect.left - 10, name_rect.top - 5, 
                         name_rect.width + 20, name_rect.height + 10))
        self.window.blit(name_text, name_rect)
        
        # Instruções
        instruction_text = self.small_font.render("ENTER para confirmar, ESC para cancelar", True, C_WHITE)
        instruction_rect = instruction_text.get_rect(center=(WIN_WIDTH // 2, 400))
        self.window.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()

    def show(self):
        """Mostra a tela de pontuações"""
        showing = True
        
        while showing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        showing = False

            self.draw_score_screen()
            self.clock.tick(60)

    def draw_score_screen(self):
        """Desenha a tela de pontuações"""
        self.window.fill((15, 15, 50))
        
        # Título
        title_text = self.font.render("MELHORES PONTUAÇÕES", True, C_YELLOW)
        title_rect = title_text.get_rect(center=(WIN_WIDTH // 2, 80))
        self.window.blit(title_text, title_rect)
        
        # Cabeçalho
        header_y = 130
        header_texts = ["POS", "NOME", "PONTOS", "MODO"]
        header_positions = [150, 300, 500, 650]
        
        for i, (text, x_pos) in enumerate(zip(header_texts, header_positions)):
            header_text = self.small_font.render(text, True, C_WHITE)
            header_rect = header_text.get_rect(center=(x_pos, header_y))
            self.window.blit(header_text, header_rect)
        
        # Linha separadora
        pygame.draw.line(self.window, C_WHITE, (100, header_y + 20), (700, header_y + 20), 2)
        
        # Pontuações
        start_y = 170
        for i, score_entry in enumerate(self.high_scores[:10]):
            y_pos = start_y + i * 35
            
            # Cor baseada na posição
            if i == 0:
                color = C_YELLOW  # Ouro
            elif i == 1:
                color = (192, 192, 192)  # Prata
            elif i == 2:
                color = (205, 127, 50)  # Bronze
            else:
                color = C_WHITE
            
            # Posição
            pos_text = self.small_font.render(f"{i+1}º", True, color)
            pos_rect = pos_text.get_rect(center=(150, y_pos))
            self.window.blit(pos_text, pos_rect)
            
            # Nome (truncar se muito longo)
            name = score_entry['name'][:15]
            name_text = self.small_font.render(name, True, color)
            name_rect = name_text.get_rect(center=(300, y_pos))
            self.window.blit(name_text, name_rect)
            
            # Pontos
            score_text = self.small_font.render(str(score_entry['score']), True, color)
            score_rect = score_text.get_rect(center=(500, y_pos))
            self.window.blit(score_text, score_rect)
            
            # Modo
            mode = score_entry['mode'].replace('NOVO JOGO ', '')[:10]
            mode_text = self.small_font.render(mode, True, color)
            mode_rect = mode_text.get_rect(center=(650, y_pos))
            self.window.blit(mode_text, mode_rect)
        
        # Mensagem se não houver pontuações
        if not self.high_scores:
            no_scores_text = self.font.render("Nenhuma pontuação ainda!", True, C_WHITE)
            no_scores_rect = no_scores_text.get_rect(center=(WIN_WIDTH // 2, 300))
            self.window.blit(no_scores_text, no_scores_rect)
        
        # Instruções
        instruction_text = self.small_font.render("Pressione ESC ou ENTER para voltar", True, C_WHITE)
        instruction_rect = instruction_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 30))
        self.window.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()

    def clear_scores(self):
        """Limpa todas as pontuações"""
        self.high_scores = []
        self.save_scores()

    def get_high_score(self):
        """Retorna a maior pontuação"""
        if self.high_scores:
            return self.high_scores[0]['score']
        return 0
