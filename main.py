import pygame
import sys
import random
from train import train_dqn_model
from env.tic_tac_toe import TicTacToeEnv
from bots.easy import EasyBot
from bots.hybrid import HybridBot
from ui.display import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic Tac Toe AI")
    model = train_dqn_model()

    while True:
        choosing = True
        bot_choice = None
        bot_player = None
        while choosing:
            draw_buttons(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 150 <= x <= 450 and 200 <= y <= 280:
                        bot_choice = EasyBot()
                        choosing = False
                    elif 150 <= x <= 450 and 320 <= y <= 400:
                        choosing = False

        env = TicTacToeEnv()
        draw_board(screen, env)
        player_turn = random.choice([True, False])
        bot_player = -1 if player_turn else 1
        if not bot_choice or not isinstance(bot_choice, EasyBot):
            bot_choice = HybridBot(model, bot_player)

        global shown_game_over
        shown_game_over = False
        in_game = True

        while in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if env.done:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            env.reset()
                            draw_board(screen, env)
                            player_turn = random.choice([True, False])
                            bot_player = -1 if player_turn else 1
                            if isinstance(bot_choice, EasyBot):
                                bot_choice = EasyBot()
                            else:
                                bot_choice = HybridBot(model, bot_player)
                            shown_game_over = False
                        elif event.key == pygame.K_m:
                            in_game = False

                elif event.type == pygame.MOUSEBUTTONDOWN and player_turn and not env.done:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // CELL, x // CELL
                    if env.board[row, col] == 0:
                        env.step((row, col))
                        draw_board(screen, env)
                        player_turn = False

            if not player_turn and not env.done:
                pygame.time.delay(300)
                env.step(bot_choice.get_action(env))
                draw_board(screen, env)
                player_turn = True

            if env.done:
                draw_game_over(screen, env, bot_player)


if __name__ == "__main__":
    main()

