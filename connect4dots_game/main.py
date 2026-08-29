"""
Connect Four - Playable GUI (Human vs AI)
--------------------------------------------
Run with: python3 main.py

Controls:
  - Move your mouse to preview a drop, click a column to play.
  - AI (alpha-beta minimax) responds automatically.
  - Press R to restart after a game ends.
  - Difficulty is set by SEARCH_DEPTH below (higher = smarter but slower).
"""

import sys
import math
import pygame

from game import Connect4, ROWS, COLS, EMPTY, PLAYER, AI
from ai import get_best_move

# --------------------------- Config ---------------------------------------
SEARCH_DEPTH = 5          # Increase for harder AI (5-7 plays well, 6+ can get slow)
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 6)

WIDTH = COLS * SQUARE_SIZE
HEIGHT = (ROWS + 1) * SQUARE_SIZE  # extra row on top for piece preview / status
SIZE = (WIDTH, HEIGHT)

BLUE = (30, 70, 180)
BLACK = (10, 10, 20)
RED = (220, 60, 60)
YELLOW = (240, 200, 40)
WHITE = (245, 245, 245)
GREY = (60, 60, 70)

pygame.init()
FONT = pygame.font.SysFont("arial", 36, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 22)


def draw_board(screen, game: Connect4):
    board = game.board
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(
                screen, BLUE,
                (c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )
            color = BLACK
            if board[r][c] == PLAYER:
                color = RED
            elif board[r][c] == AI:
                color = YELLOW
            pygame.draw.circle(
                screen, color,
                (c * SQUARE_SIZE + SQUARE_SIZE // 2, (r + 1) * SQUARE_SIZE + SQUARE_SIZE // 2),
                RADIUS
            )
    pygame.display.update()


def draw_top_row(screen, posx, current_turn):
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
    if current_turn == PLAYER:
        pygame.draw.circle(screen, RED, (posx, SQUARE_SIZE // 2), RADIUS)


def draw_message(screen, text, color):
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
    label = FONT.render(text, True, color)
    rect = label.get_rect(center=(WIDTH // 2, SQUARE_SIZE // 2))
    screen.blit(label, rect)
    pygame.display.update()


def main():
    game = Connect4()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Connect Four - Minimax AI (Alpha-Beta)")
    draw_board(screen, game)

    turn = PLAYER  # Human goes first
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION and not game_over and turn == PLAYER:
                posx = event.pos[0]
                draw_top_row(screen, posx, turn)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and turn == PLAYER:
                posx = event.pos[0]
                col = posx // SQUARE_SIZE
                if game.is_valid_move(col):
                    game.drop_piece(col, PLAYER)
                    turn = AI

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game = Connect4()
                turn = PLAYER
                game_over = False
                draw_board(screen, game)

        draw_board(screen, game)

        if game.game_over and not game_over:
            game_over = True
            if game.winner == PLAYER:
                draw_message(screen, "You win! Press R to restart", RED)
            elif game.winner == AI:
                draw_message(screen, "AI wins! Press R to restart", YELLOW)
            else:
                draw_message(screen, "Draw! Press R to restart", WHITE)

        if not game_over and turn == AI:
            pygame.time.wait(250)  # brief pause so the move doesn't feel instant
            col = get_best_move(game, SEARCH_DEPTH)
            if col is not None:
                game.drop_piece(col, AI)
            turn = PLAYER

        pygame.time.wait(10)


if __name__ == "__main__":
    main()
