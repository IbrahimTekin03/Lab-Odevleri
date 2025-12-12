import pygame
import sys
import os
import random
from buckshot_game import launch_buckshot_game
import buckshot_game_2player  # Dosyanın başında import etmeyi unutma

FPS = 60


WHITE = (255, 255, 255)
RED = (200, 0, 0)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
THEME_GREEN = (30, 130, 30)
FRAME_COLOR = (40, 40, 40)
HIGHLIGHT_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (60, 60, 60)


TITLE_SIZE = 64
BUTTON_SIZE = 36


ASSETS_PATH = os.path.join("assets", "images")
BG_IMAGE_PATH = os.path.join(ASSETS_PATH, "game_background.png")
HOVER_SFX_PATH = os.path.join("assets", "sounds", "Button.wav")
CLICK_SFX_PATH = os.path.join("assets", "sounds", "ButtonClick.wav")
OST_PATH = os.path.join("assets", "sounds", "GameOst.wav")

# Pygame'i baslat
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Click of Fate")
clock = pygame.time.Clock()

# Fontlar
font_title = pygame.font.SysFont("arial", TITLE_SIZE, bold=True)
font_button = pygame.font.SysFont("arial", BUTTON_SIZE)

# Karakter klasörü (pygame.init sonra olmalı)
CHARACTER_IMAGES = [f for f in os.listdir(ASSETS_PATH) if f.startswith("char") and f.endswith(".png")]
CHARACTER_IMAGES.sort()
characters = [pygame.image.load(os.path.join(ASSETS_PATH, img)).convert_alpha() for img in CHARACTER_IMAGES]
characters = [pygame.transform.smoothscale(img, (300, 400)) for img in characters]

# Ses
try:
    hover_sound = pygame.mixer.Sound(HOVER_SFX_PATH)
    hover_sound.set_volume(0.2)
    click_sound = pygame.mixer.Sound(CLICK_SFX_PATH)
    click_sound.set_volume(0.2)
    pygame.mixer.music.load(OST_PATH)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
except:
    hover_sound = None
    click_sound = None

hovered_buttons = {
    "start": False,
    "options": False,  # burayı ekle
    "back": False,
}

music_enabled = True

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def character_selection_menu():
    current_index = 0
    selected = False
    left_arrow = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 50, 50, 100)
    right_arrow = pygame.Rect(WIDTH // 2 + 200, HEIGHT // 2 - 50, 50, 100)
    start_button = pygame.Rect(WIDTH // 2 - 220, HEIGHT - 130, 200, 60)
    back_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 130, 200, 60)

    while not selected:
        screen.fill((10, 10, 10))
        draw_text("Karakter Seç", font_title, RED, screen, WIDTH // 2, 100)

        pygame.draw.polygon(screen, WHITE, [(left_arrow.right, left_arrow.top), (left_arrow.left, left_arrow.centery), (left_arrow.right, left_arrow.bottom)])
        pygame.draw.polygon(screen, WHITE, [(right_arrow.left, right_arrow.top), (right_arrow.right, right_arrow.centery), (right_arrow.left, right_arrow.bottom)])

        character = characters[current_index]
        character_rect = character.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        frame_rect = character_rect.inflate(30, 30)
        pygame.draw.rect(screen, FRAME_COLOR, frame_rect, border_radius=16)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, frame_rect, 2, border_radius=16)
        screen.blit(character, character_rect)

        mx, my = pygame.mouse.get_pos()
        if start_button.collidepoint((mx, my)):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, start_button, border_radius=12)
        else:
            pygame.draw.rect(screen, DARK_GRAY, start_button, border_radius=12)

        if back_button.collidepoint((mx, my)):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, back_button, border_radius=12)
        else:
            pygame.draw.rect(screen, DARK_GRAY, back_button, border_radius=12)

        draw_text("Oyuna Başla", font_button, WHITE, screen, start_button.centerx, start_button.centery)
        draw_text("Geri Dön", font_button, WHITE, screen, back_button.centerx, back_button.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_sound: click_sound.play()
                if left_arrow.collidepoint(event.pos):
                    current_index = (current_index - 1) % len(characters)
                elif right_arrow.collidepoint(event.pos):
                    current_index = (current_index + 1) % len(characters)
                elif start_button.collidepoint(event.pos):
                    player_index = current_index
                    selected_path = os.path.join(ASSETS_PATH, f"char{player_index}.png")
                    pygame.quit()

                    launch_buckshot_game(player_image_path=selected_path)
                    sys.exit()


            elif back_button.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(FPS)

def character_selection_menu_2p():
    index_p1 = 0
    index_p2 = 1
    selected = False
    start_button = pygame.Rect(WIDTH // 2 - 220, HEIGHT - 130, 200, 60)
    back_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 130, 200, 60)

    while not selected:
        screen.fill((10, 10, 10))
        draw_text("Karakter Seç (2 Oyuncu)", font_title, RED, screen, WIDTH // 2, 80)

        # Player 1
        char1 = characters[index_p1]
        rect1 = char1.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        frame1 = rect1.inflate(30, 30)
        pygame.draw.rect(screen, FRAME_COLOR, frame1, border_radius=16)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, frame1, 2, border_radius=16)
        screen.blit(char1, rect1)
        draw_text("Oyuncu 1", font_button, WHITE, screen, rect1.centerx, rect1.top - 40)

        # Arrows P1
        left_arrow_p1 = pygame.Rect(rect1.left - 60, rect1.centery - 40, 40, 80)
        right_arrow_p1 = pygame.Rect(rect1.right + 20, rect1.centery - 40, 40, 80)
        pygame.draw.polygon(screen, WHITE, [(left_arrow_p1.right, left_arrow_p1.top), (left_arrow_p1.left, left_arrow_p1.centery), (left_arrow_p1.right, left_arrow_p1.bottom)])
        pygame.draw.polygon(screen, WHITE, [(right_arrow_p1.left, right_arrow_p1.top), (right_arrow_p1.right, right_arrow_p1.centery), (right_arrow_p1.left, right_arrow_p1.bottom)])

        # Player 2
        char2 = characters[index_p2]
        rect2 = char2.get_rect(center=(WIDTH * 3 // 4, HEIGHT // 2))
        frame2 = rect2.inflate(30, 30)
        pygame.draw.rect(screen, FRAME_COLOR, frame2, border_radius=16)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, frame2, 2, border_radius=16)
        screen.blit(char2, rect2)
        draw_text("Oyuncu 2", font_button, WHITE, screen, rect2.centerx, rect2.top - 40)

        # Arrows P2
        left_arrow_p2 = pygame.Rect(rect2.left - 60, rect2.centery - 40, 40, 80)
        right_arrow_p2 = pygame.Rect(rect2.right + 20, rect2.centery - 40, 40, 80)
        pygame.draw.polygon(screen, WHITE, [(left_arrow_p2.right, left_arrow_p2.top), (left_arrow_p2.left, left_arrow_p2.centery), (left_arrow_p2.right, left_arrow_p2.bottom)])
        pygame.draw.polygon(screen, WHITE, [(right_arrow_p2.left, right_arrow_p2.top), (right_arrow_p2.right, right_arrow_p2.centery), (right_arrow_p2.left, right_arrow_p2.bottom)])

        mx, my = pygame.mouse.get_pos()
        for btn, key in [(start_button, "start"), (back_button, "back")]:
            if btn.collidepoint((mx, my)):
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, btn, border_radius=12)
                if not hovered_buttons[key]:
                    if hover_sound: hover_sound.play()
                    hovered_buttons[key] = True
            else:
                pygame.draw.rect(screen, DARK_GRAY, btn, border_radius=12)
                hovered_buttons[key] = False

        draw_text("Oyuna Başla", font_button, WHITE, screen, start_button.centerx, start_button.centery)
        draw_text("Geri Dön", font_button, WHITE, screen, back_button.centerx, back_button.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_a:
                    index_p1 = (index_p1 - 1) % len(characters)
                elif event.key == pygame.K_d:
                    index_p1 = (index_p1 + 1) % len(characters)
                elif event.key == pygame.K_LEFT:
                    index_p2 = (index_p2 - 1) % len(characters)
                elif event.key == pygame.K_RIGHT:
                    index_p2 = (index_p2 + 1) % len(characters)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_sound: click_sound.play()
                if left_arrow_p1.collidepoint(event.pos):
                    index_p1 = (index_p1 - 1) % len(characters)
                elif right_arrow_p1.collidepoint(event.pos):
                    index_p1 = (index_p1 + 1) % len(characters)
                elif left_arrow_p2.collidepoint(event.pos):
                    index_p2 = (index_p2 - 1) % len(characters)
                elif right_arrow_p2.collidepoint(event.pos):
                    index_p2 = (index_p2 + 1) % len(characters)
                elif start_button.collidepoint(event.pos) and index_p1 != index_p2:
                    print(f"PLAYER 1: char{index_p1}.png vs PLAYER 2: char{index_p2}.png")
                    pygame.quit()
                    player1_path = os.path.join(ASSETS_PATH, f"char{index_p1}.png")
                    player2_path = os.path.join(ASSETS_PATH, f"char{index_p2}.png")
                    buckshot_game_2player.launch_buckshot_game_2player(player1_path, player2_path)
                    sys.exit()
                elif back_button.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(FPS)



def confirm_quit():
    confirmation = True
    while confirmation:
        screen.fill((0, 0, 0))
        draw_text("Oyundan çıkmak istediğinizden emin misiniz?", font_button, WHITE, screen, WIDTH // 2, HEIGHT // 3)
        yes_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT // 2, 120, 60)
        no_button = pygame.Rect(WIDTH // 2 + 40, HEIGHT // 2, 120, 60)
        mx, my = pygame.mouse.get_pos()
        pygame.draw.rect(screen, RED if yes_button.collidepoint((mx, my)) else DARK_GRAY, yes_button, border_radius=15)
        pygame.draw.rect(screen, RED if no_button.collidepoint((mx, my)) else DARK_GRAY, no_button, border_radius=15)
        draw_text("Evet", font_button, WHITE, screen, yes_button.centerx, yes_button.centery)
        draw_text("Hayır", font_button, WHITE, screen, no_button.centerx, no_button.centery)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint((mx, my)): pygame.quit(); sys.exit()
                if no_button.collidepoint((mx, my)): confirmation = False
        pygame.display.flip()
        clock.tick(FPS)


def mode_selection_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text("Mod Seç", font_title, RED, screen, WIDTH // 2, HEIGHT // 6)
        mx, my = pygame.mouse.get_pos()
        button_bot = pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2 - 60, 250, 60)
        button_2p = pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2 + 20, 250, 60)
        button_back = pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2 + 100, 250, 60)
        pygame.draw.rect(screen, RED if button_bot.collidepoint((mx, my)) else GRAY, button_bot, border_radius=12)
        pygame.draw.rect(screen, RED if button_2p.collidepoint((mx, my)) else GRAY, button_2p, border_radius=12)
        pygame.draw.rect(screen, RED if button_back.collidepoint((mx, my)) else GRAY, button_back, border_radius=12)
        draw_text("PLAYER vs BOT", font_button, WHITE, screen, button_bot.centerx, button_bot.centery)
        draw_text("2 PLAYER", font_button, WHITE, screen, button_2p.centerx, button_2p.centery)
        draw_text("Geri Dön", font_button, WHITE, screen, button_back.centerx, button_back.centery)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_sound: click_sound.play()
                if button_bot.collidepoint((mx, my)):
                    character_selection_menu()
                    running = False
                elif button_2p.collidepoint((mx, my)):
                    character_selection_menu_2p()
                    running = False
                elif button_back.collidepoint((mx, my)):
                    running = False
        pygame.display.flip()
        clock.tick(FPS)


def settings_menu():
    global music_enabled
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text("SEÇENEKLER", font_title, RED, screen, WIDTH // 2, HEIGHT // 6)
        mx, my = pygame.mouse.get_pos()
        button_music = pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2 - 60, 250, 60)
        button_back = pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2 + 50, 250, 60)
        pygame.draw.rect(screen, RED if button_music.collidepoint((mx, my)) else GRAY, button_music, border_radius=12)
        pygame.draw.rect(screen, RED if button_back.collidepoint((mx, my)) else GRAY, button_back, border_radius=12)
        music_text = "Müziği Kapat" if music_enabled else "Müziği Aç"
        draw_text(music_text, font_button, WHITE, screen, button_music.centerx, button_music.centery)
        draw_text("Geri Dön", font_button, WHITE, screen, button_back.centerx, button_back.centery)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: confirm_quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_sound: click_sound.play()
                if button_music.collidepoint((mx, my)):
                    music_enabled = not music_enabled
                    pygame.mixer.music.set_volume(0.1 if music_enabled else 0.0)
                if button_back.collidepoint((mx, my)):
                    running = False
        pygame.display.flip()
        clock.tick(FPS)

def main_menu():
    bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
    bg_image = pygame.transform.smoothscale(bg_image, (WIDTH, HEIGHT))
    while True:
        screen.blit(bg_image, (0, 0))
        mx, my = pygame.mouse.get_pos()
        button_width, button_height = 400, 70
        right_margin = 100  # Sağdan boşluk

        button_start = pygame.Rect(WIDTH - button_width - right_margin, HEIGHT // 2 - 90, button_width, button_height)
        button_options = pygame.Rect(WIDTH - button_width - right_margin, HEIGHT // 2, button_width, button_height)
        button_quit = pygame.Rect(WIDTH - button_width - right_margin, HEIGHT // 2 + 90, button_width, button_height)

        buttons = [("start", button_start), ("options", button_options), ("quit", button_quit)]
        for key, button in buttons:
            if button.collidepoint((mx, my)):
                pygame.draw.rect(screen, RED, button, border_radius=16)
                if not hovered_buttons[key]:
                    if hover_sound: hover_sound.play()
                    hovered_buttons[key] = True
            else:
                pygame.draw.rect(screen, DARK_GRAY, button, border_radius=16)
                hovered_buttons[key] = False
        draw_text("Oyuna Başla", font_button, WHITE, screen, button_start.centerx, button_start.centery)
        draw_text("Seçenekler", font_button, WHITE, screen, button_options.centerx, button_options.centery)
        draw_text("Çıkış", font_button, WHITE, screen, button_quit.centerx, button_quit.centery)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: confirm_quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_sound: click_sound.play()
                if button_start.collidepoint((mx, my)): mode_selection_menu()
                if button_options.collidepoint((mx, my)): settings_menu()
                if button_quit.collidepoint((mx, my)): confirm_quit()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":

    main_menu()