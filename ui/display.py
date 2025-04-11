import pygame

WIDTH = HEIGHT = 600
CELL = WIDTH // 3
LINE = (30, 30, 30)
CROSS = (0, 0, 0)
CIRCLE = (0, 120, 255)
BG = (220, 240, 255)
BTN_COLOR = (100, 180, 255)

font = pygame.font.SysFont(None, 50)

def draw_board(screen, env):
    screen.fill(BG)
    for i in range(1, 3):
        pygame.draw.line(screen, LINE, (0, i * CELL), (WIDTH, i * CELL), 3)
        pygame.draw.line(screen, LINE, (i * CELL, 0), (i * CELL, HEIGHT), 3)
    for r in range(3):
        for c in range(3):
            mark = env.board[r][c]
            cx = c * CELL + CELL // 2
            cy = r * CELL + CELL // 2
            if mark == 1:
                pygame.draw.line(screen, CROSS, (cx - 40, cy - 40), (cx + 40, cy + 40), 6)
                pygame.draw.line(screen, CROSS, (cx - 40, cy + 40), (cx + 40, cy - 40), 6)
            elif mark == -1:
                pygame.draw.circle(screen, CIRCLE, (cx, cy), 40, 6)
    pygame.display.update()

def draw_text(screen, text, size=50, y=HEIGHT//2, center=True):
    f = pygame.font.SysFont(None, size)
    txt = f.render(text, True, LINE)
    rect = txt.get_rect(center=(WIDTH // 2, y) if center else (20, y))
    screen.blit(txt, rect)


def draw_buttons(screen):
    screen.fill(BG)
    pygame.draw.rect(screen, BTN_COLOR, (150, 200, 300, 80))
    pygame.draw.rect(screen, BTN_COLOR, (150, 320, 300, 80))
    draw_text(screen, "Easy Bot", 50, 240)
    draw_text(screen, "Hybrid Bot", 50, 360)
    draw_text(screen, "Choose Difficulty", 60, 100)
    pygame.display.update()

def draw_game_over(screen, env, bot_player, player_score, bot_score, shown_game_over):
    if shown_game_over:
        return player_score, bot_score, True
    if env.winner == bot_player:
        bot_score += 1
        draw_text(screen, "Bot wins!", 70)
    elif env.winner == -bot_player:
        player_score += 1
        draw_text(screen, "You win!", 70)
    else:
        draw_text(screen, "It's a draw!", 70)
    draw_text(screen, f"Score: You {player_score} - {bot_score} Bot", 40, HEIGHT // 2 + 40)
    draw_text(screen, "Press R to replay", 30, HEIGHT // 2 + 90)
    draw_text(screen, "Press M for menu", 30, HEIGHT // 2 + 130)
    pygame.display.update()
    return player_score, bot_score, True
