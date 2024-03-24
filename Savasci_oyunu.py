import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

savasci_simgeleri = {
    "Muhafız": "M",
    "Okçu": "O",
    "Topçu": "T",
    "Atlı": "A",
    "Sağlıkçı": "S"
}

# Oyuncu sınıfı
class Player:
    def __init__(self, name, color, baslangic_pozisyonu):
        self.name = name
        self.color = color
        self.kaynaklar = 200
        self.savascilar = []
        self.can = 1
        self.baslangic_pozisyonu = baslangic_pozisyonu
        self.kaynak = 200
        self.tur_sayaci = 0
        self.yerlestirilen_savasci_sayisi = 0
        self.hamle_sayisi = 0


    def kaynak_ekle(self, miktar):
        self.kaynaklar += miktar
        self.kaynak += miktar

    def spend_resources(self, miktar):
        if self.kaynaklar >= miktar:
            self.kaynaklar -= miktar
            return True
        return False

    def update_resources(self, world):

        self.tur_sayaci += 1

        if self.tur_sayaci % 8 == 0:

            self.kaynak_ekle(10 + len(self.savascilar))

    def dongu(self):
        self.yerlestirilen_savasci_sayisi = 0
        self.hamle_sayisi += 1

class Savasci:
    def __init__(self, isim, can, hedef_sayisi, hasar, menzil_x, menzil_y, capraz, x=0, y=0):
        self.isim = isim
        self.health = can
        self.hedef_sayisi = hedef_sayisi
        self.damage_modifier = hasar
        self.menzil_x = menzil_x
        self.range_y = menzil_y
        self.capraz = capraz
        self.pozisyon_x = x
        self.pozisyon_y = y


WARRIOR_PROPERTIES = {
    "Muhafız": Savasci("Muhafız", 80, None, 20, 1, 1, 1, x=0, y=0),
    "Okçu": Savasci("Okçu", 30, 3, -0.6, 2, 2, 2, x=0, y=0),
    "Topçu": Savasci("Topçu", 30, 1, -1.0, 2, 2, 0, x=0, y=0),
    "Atlı": Savasci("Atlı", 40, 2, -30, 0, 0, 3, x=0, y=0),
    "Sağlıkçı": Savasci("Sağlıkçı", 100, 3, 0.5, 2, 2, 2, x=0, y=0)
}

# Dünya sınıfı
class World:
    def __init__(self, size):
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.grid[0][0] = "M1"
        self.grid[0][size - 1] = "M2"
        self.grid[size - 1][0] = "M3"
        self.grid[size - 1][size - 1] = "M4"

    def display(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell != '.':
                    player_name = str(cell)
                    if player_name in PLAYERS:
                        color = PLAYERS[player_name].color
                    else:
                        print(f"Invalid player name: {player_name}")
                        color = WHITE

                    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                    if (x == 0 and y == 0) or (x == 0 and y == self.size - 1):
                        text = font.render("M1" if y == 0 else "M2", True, BLACK)
                        text_rect = text.get_rect(
                            center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
                        screen.blit(text, text_rect)
                    elif (x == self.size - 1 and y == 0) or (x == self.size - 1 and y == self.size - 1):
                        text = font.render("M3" if y == 0 else "M4", True, BLACK)
                        text_rect = text.get_rect(
                            center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
                        screen.blit(text, text_rect)

                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


WARRIOR_COSTS = {
    "Muhafız": 10,
    "Okçu": 20,
    "Topçu": 50,
    "Atlı": 30,
    "Sağlıkçı": 10
}


def oyun_bitis_kontrolu(players, world):
    alive_players = [player for player in players.values() if any(warrior.health > 0 for warrior in player.savascilar)]

    if len(alive_players) == 1:
        print(f"{alive_players[0].name} kazandı!")
        return True

    for player_name, player in players.items():
        if passed_turn_count[player_name] >= 3:
            print(f"{player.name} 3 el üst üste pas geçti ve oyunu kaybetti!")
            return True

    total_cells = world.size * world.size
    for player_name, player in players.items():
        warrior_count = sum(1 for warrior in player.savascilar if warrior.health > 0)
        if warrior_count / total_cells >= 0.6:
            print(f"{player.name} oyunun %60'ını ele geçirdi ve kazandı!")
            return True

    return False


def create_warrior_buttons():
    button_width = 150
    button_height = 50
    margin = 10
    x = SCREEN_WIDTH + 10
    y = SCREEN_HEIGHT - button_height - margin
    buttons = []

    savasci_listesini_ters_dondur = list(savasci_simgeleri.keys())[::-1]

    for i, warrior_type in enumerate(savasci_listesini_ters_dondur):
        icon = savasci_simgeleri[warrior_type]
        button_rect = pygame.Rect(x, y - i * (button_height + margin), button_width, button_height)
        button_color = (150, 150, 150)
        buttons.append((button_rect, warrior_type, icon, button_color))

    return buttons


def create_pass_button():
    button_width = 150
    button_height = 50
    x = SCREEN_WIDTH + 10
    y = SCREEN_HEIGHT - button_height - 400
    button_rect = pygame.Rect(x, y, button_width, button_height)
    button_color = (200, 200, 200)
    return button_rect, button_color

def create_start_battle_button():
    button_width = 150
    button_height = 50
    x = SCREEN_WIDTH + 10
    y = SCREEN_HEIGHT - button_height - 550
    button_rect = pygame.Rect(x, y, button_width, button_height)
    button_color = (200, 200, 200)
    return button_rect, button_color


def draw_start_battle_button():
    pygame.draw.rect(screen, start_battle_button_color, start_battle_button_rect)
    start_battle_text = font.render("Savaş Başlat", True, BLACK)
    screen.blit(start_battle_text, (
        start_battle_button_rect.centerx - start_battle_text.get_width() // 2,
        start_battle_button_rect.centery - start_battle_text.get_height() // 2))


def start_battle():
    for player_name in PLAYER_ORDER:
        current_player = PLAYERS[player_name]
        opponent_name = next(opponent for opponent in PLAYER_ORDER if opponent != player_name)
        opponent_player = PLAYERS[opponent_name]

        for placed_warrior_type, (placed_x, placed_y) in placed_warriors[player_name]:
            placed_warrior = WARRIOR_PROPERTIES[placed_warrior_type]
            for opponent_warrior_type, (opponent_x, opponent_y) in placed_warriors[opponent_name]:
                opponent_warrior = WARRIOR_PROPERTIES[opponent_warrior_type]

                if (placed_warrior.menzil_x >= abs(placed_x - opponent_x) and
                        placed_warrior.range_y >= abs(placed_y - opponent_y)):

                    damage = random.randint(1, 10)

                    opponent_warrior.health -= damage
                    print(f"{placed_warrior_type} attacked {opponent_warrior_type} and dealt {damage} damage.")


def place_random_warrior(player, world):
    available_cells = []

    for y in range(world.size):
        for x in range(world.size):
            if can_place_warrior(x, y, player.name, world):
                available_cells.append((x, y))

    if available_cells:
        x, y = random.choice(available_cells)

        warrior_type = random.choice(list(savasci_simgeleri.keys()))

        if warrior_type and player.spend_resources(WARRIOR_COSTS[warrior_type]):
            player.savascilar.append(warrior_type)
            world.grid[y][x] = savasci_simgeleri[warrior_type]
            print(f"{player.name} rastgele {warrior_type} savaşçısını ({x}, {y}) koordinatına yerleştirdi.")


def initiate_combat(attacker, defender):

    random_damage = random.randint(1, 10)

    if (attacker.menzil_x >= abs(attacker.pozisyon_x - defender.pozisyon_x) and
            attacker.range_y >= abs(attacker.pozisyon_y - defender.pozisyon_y) and
            attacker.health > 0 and defender.health > 0):

        damage = attacker.damage_modifier + random_damage

        defender.health -= damage

        print(f"{attacker.name} attacked {defender.name} and dealt {damage} damage.")

        if defender.health <= 0:
            defender.health = 0
            print(f"{defender.name} has been defeated!")
    else:
        print(f"{attacker.name} cannot attack {defender.name}. Out of range or one of them is defeated.")

pygame.init()

world_size = 0
while True:
    size = input("Dünya boyutunu girin (örn: 8, 16, 24, 32): ")
    if size.isdigit():
        size = int(size)
        if 8 <= size <= 32:
            world_size = size
            break
    print("Geçersiz giriş! Boyut 8 ile 32 arasında olmalıdır.")

CELL_SIZE = 800 // world_size
SCREEN_WIDTH = CELL_SIZE * world_size
SCREEN_HEIGHT = CELL_SIZE * world_size

screen = pygame.display.set_mode((SCREEN_WIDTH + 200, SCREEN_HEIGHT))
pygame.display.set_caption("Warrior Placement")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

world = World(world_size)

PLAYER_COLORS = [RED, BLUE, GREEN, YELLOW]
PLAYERS = {str(i+1): Player(f"Player {i + 1}", PLAYER_COLORS[i], (0 if i < 2 else world_size - 1, 0 if i % 2 == 0 else world_size - 1)) for i in range(4)}

for player in PLAYERS.values():
    x, y = player.baslangic_pozisyonu
    world.grid[y][x] = player.name[7]

PLAYER_ORDER = list(PLAYERS.keys())
placed_warriors = {player_name: [] for player_name in PLAYERS}
passed_turn_count = 0

warrior_buttons = create_warrior_buttons()

def display_treasures(players):
    treasure_font = pygame.font.SysFont(None, 24)
    x_offset = SCREEN_WIDTH + 20
    y_offset = 60
    for i, player in enumerate(players.values()):
        treasure_text = treasure_font.render(f"{player.name} Hazinesi: {player.kaynak}", True, BLACK)
        screen.blit(treasure_text, (x_offset, y_offset + i * 30))

def can_place_warrior(x, y, player_name, world):

    if x < 0 or x >= world.size or y < 0 or y >= world.size:
        return False
    if world.grid[y][x] != '.':
        return False

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            nx, ny = x + i, y + j
            if 0 <= nx < world.size and 0 <= ny < world.size and world.grid[ny][nx] == player_name[7]:
                return True
    return False

running = True
selected_warrior = None
clicked_once = False
current_player_index = 0
printed_current_player = False
printed_available_coordinates = False
pass_button, pass_button_color = create_pass_button()
start_battle_button_rect, start_battle_button_color = create_start_battle_button()

while running:
    screen.fill(WHITE)
    world.display(screen)
    for button_rect, warrior_type, _, button_color in warrior_buttons:
        pygame.draw.rect(screen, button_color, button_rect)
        warrior_text = font.render(warrior_type, True, BLACK)
        screen.blit(warrior_text, (
            button_rect.centerx - warrior_text.get_width() // 2, button_rect.centery - warrior_text.get_height() // 2))

    pygame.draw.rect(screen, pass_button_color, pass_button)
    pass_text = font.render("Pas Geç", True, BLACK)
    screen.blit(pass_text, (
        pass_button.centerx - pass_text.get_width() // 2, pass_button.centery - pass_text.get_height() // 2))

    draw_start_battle_button()

    current_player = PLAYERS[PLAYER_ORDER[current_player_index]]

    if not printed_current_player:
        print(f"Sıra: {PLAYERS[PLAYER_ORDER[current_player_index]].name}")
        printed_current_player = True

    for player in PLAYERS.values():
        player.hamle_sayisi = 0

    placed_warriors = {player_name: [] for player_name in PLAYERS}

    for _ in range(5):
        for player_name in PLAYER_ORDER:
            current_player = PLAYERS[player_name]
            opponent_name = next(opponent for opponent in PLAYER_ORDER if opponent != player_name)
            opponent_player = PLAYERS[opponent_name]

            for warrior_type, coordinates in placed_warriors[player_name]:
                warrior = WARRIOR_PROPERTIES[warrior_type]
                x, y = coordinates

                if warrior.move_count < 5:
                    for opponent_warrior_type, opponent_coordinates in placed_warriors[opponent_name]:
                        opponent_warrior = WARRIOR_PROPERTIES[opponent_warrior_type]
                        opponent_x, opponent_y = opponent_coordinates

                        if (warrior.menzil_x >= abs(x - opponent_x) and
                                warrior.range_y >= abs(y - opponent_y)):
                            initiate_combat(warrior, opponent_warrior)

                            warrior.move_count += 1
                            opponent_warrior.move_count += 1

                            if warrior.health <= 0:
                                print(f"{warrior.isim} has been defeated!")

                                placed_warriors[player_name].remove((warrior_type, coordinates))
                            if opponent_warrior.health <= 0:
                                print(f"{opponent_warrior.isim} has been defeated!")

                                placed_warriors[opponent_name].remove((opponent_warrior_type, opponent_coordinates))

    display_treasures(PLAYERS)
    current_player = PLAYERS[PLAYER_ORDER[current_player_index]]

    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if start_battle_button_rect.collidepoint(mouse_x, mouse_y):
            start_battle()

        if passed_turn:
            passed_turn_count += 1
        if pass_button.collidepoint(mouse_x, mouse_y) and not passed_turn:
            current_player_index = (current_player_index + 1) % len(PLAYER_ORDER)
            printed_current_player = False
            passed_turn = True

        for button_rect, warrior_type, _, _ in warrior_buttons:
            if button_rect.collidepoint(mouse_x, mouse_y):
                if selected_warrior != warrior_type:
                    selected_warrior = warrior_type
                    print(f"Savaşçı {selected_warrior} seçildi.")
                    break

            else:
                if not clicked_once and 0 <= mouse_x < SCREEN_WIDTH and 0 <= mouse_y < SCREEN_HEIGHT:
                    clicked_x = mouse_x // CELL_SIZE
                    clicked_y = mouse_y // CELL_SIZE

                    if selected_warrior:

                        text = font.render(savasci_simgeleri[selected_warrior], True, BLACK)
                        screen.blit(text, (
                            clicked_x * CELL_SIZE + CELL_SIZE // 3, clicked_y * CELL_SIZE + CELL_SIZE // 3))
                        current_player = PLAYERS[PLAYER_ORDER[current_player_index]]
                        if can_place_warrior(clicked_x, clicked_y, current_player.name, world):

                            cost = {
                                "Muhafız": 10,
                                "Okçu": 20,
                                "Topçu": 50,
                                "Atlı": 30,
                                "Sağlıkçı": 10
                            }

                            if current_player.kaynaklar >= cost[selected_warrior]:

                                if current_player.spend_resources(cost[selected_warrior]):

                                    icon_text = font.render(savasci_simgeleri[selected_warrior], True, BLACK)
                                    screen.blit(icon_text, (
                                        clicked_x * CELL_SIZE + CELL_SIZE // 3, clicked_y * CELL_SIZE + CELL_SIZE // 3))

                                    current_player.savascilar.append(selected_warrior)

                                    text = font.render(savasci_simgeleri[selected_warrior], True, BLACK)
                                    screen.blit(text, (
                                        clicked_x * CELL_SIZE + CELL_SIZE // 3, clicked_y * CELL_SIZE + CELL_SIZE // 3))

                                    world.grid[clicked_y][clicked_x] = current_player.name[7]

                                    current_player.kaynak -= cost[selected_warrior]

                                    current_player.yerlestirilen_savasci_sayisi += 1

                                    pygame.display.update()

                                    print(f"({clicked_x}, {clicked_y}) koordinatlı alana {selected_warrior} ekledi.")

                                    if all(player.hamle_sayisi >= 5 for player in PLAYERS.values()):
                                        print("Savaş başlıyor!")

                                        for player in PLAYERS.values():
                                            for warrior in player.savascilar:

                                                opponent_player = next(
                                                    opponent for opponent in PLAYERS.values() if opponent != player)
                                                initiate_combat(WARRIOR_PROPERTIES["Muhafız"], opponent_player)

                                        for player in PLAYERS.values():
                                            player.hamle_sayisi = 0

                                    if len(current_player.savascilar) == 2 or current_player.yerlestirilen_savasci_sayisi == 2:
                                        current_player.dongu()
                                        current_player_index = (current_player_index + 1) % len(PLAYER_ORDER)
                                        printed_current_player = False
                                        printed_available_coordinates = False
                                        selected_warrior = None
                                        clicked_once = True

                                    for player in PLAYERS.values():
                                        player.update_resources(world)
                                else:
                                    print("Yetersiz kaynak!")
                            else:
                                print("Savaşçı limitine ulaşıldı!")

                        clicked_once = True

        else:
            clicked_once = False

    else:
        passed_turn = False

    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if start_battle_button_rect.collidepoint(mouse_x, mouse_y):
                start_battle()

    if not printed_available_coordinates:
        current_player_name = PLAYERS[PLAYER_ORDER[current_player_index]].name
        print(f"{current_player_name} için koyabileceğiniz koordinatlar:")
        for y in range(world.size):
            for x in range(world.size):
                if can_place_warrior(x, y, current_player_name, world):
                    print(f"({x}, {y})")
        printed_available_coordinates = True

pygame.quit()