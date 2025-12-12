import sys, random, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QTransform, QFont, QPainter

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os


class Shell:
    def __init__(self, shell_type):
        self.type = shell_type  # 'live' or 'blank'
        self.visible = False



class Item(QLabel):
    def __init__(self, parent, item_type, image_path, index):
        super().__init__(parent)
        self.item_type = item_type
        self.used = False
        self.setPixmap(QPixmap(image_path).scaled(80, 80))  # Büyütüldü
        self.setFixedSize(80, 80)
        self.setScaledContents(True)


    def mark_used(self):
        self.setStyleSheet("opacity: 0.3; background: transparent")
        self.used = True

class GameWindow(QWidget):
    def __init__(self, player_image_path=None, opponent_image_path=None):
        super().__init__()

        self.is_two_player = True  # BU SATIR EKLENDİ

        self.player_image_path = player_image_path
        self.opponent_image_path = opponent_image_path

        self.player_image_path = player_image_path
        self.opponent_image_path = opponent_image_path
        self.setWindowTitle("Buckshot Roulette")
        self.setGeometry(300, 100, 800, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.shells = []
        self.chamber_index = 0
        self.turn = 0
        self.game_over = False
        self.player_blocked = False
        self.opponent_blocked = False

        self.player_hearts = []
        self.opponent_hearts = []
        self.player_lives = 1  # Can sayısı başlangıç
        self.opponent_lives = 1

        # Diğer değişkenler
        self.player_health = 1
        self.opponent_health = 1
        self.player1_shot_rights = 2
        self.player2_shot_rights = 2

        # QMediaPlayer ile ses efekti yükle
        self.shotgun_player = QMediaPlayer()
        sound_path = os.path.join(os.path.dirname(__file__), "shotgun.wav")
        self.shotgun_player.setMedia(QMediaContent(QUrl.fromLocalFile(sound_path)))
        self.shotgun_player.setVolume(80)  # 0-100 arası bir ses seviyesi

        # Boş mermi sesi için yeni player
        self.empty_player = QMediaPlayer()
        empty_sound_path = os.path.join(os.path.dirname(__file__), "empty.wav")
        self.empty_player.setMedia(QMediaContent(QUrl.fromLocalFile(empty_sound_path)))
        self.empty_player.setVolume(80)

        self.is_first_round = True
        self.items = []
        self.item_types = ['xray', 'heal', 'block']
        self.init_ui()

        heart_size = 40
        # Oyuncu kalpleri (sol alt köşeye yakın)
        start_x_player = 20
        y_player = self.height() - 80

        # Oyuncu kalpleri sadece oluşturuluyor
        for i in range(3):
            heart = QLabel(self)
            heart.setPixmap(QPixmap("assets/images/heart_full.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            heart.setFixedSize(40, 40)
            heart.show()
            self.player_hearts.append(heart)

        # Rakip kalpleri sadece oluşturuluyor
        for i in range(3):
            heart = QLabel(self)
            heart.setPixmap(QPixmap("assets/images/heart_full.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            heart.setFixedSize(40, 40)
            heart.show()
            self.opponent_hearts.append(heart)

        self.reset_game()

    def init_ui(self):
        screen_rect = QApplication.primaryScreen().geometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Yeni daha büyük fontlar
        font_info = QFont("Arial", 24, QFont.Bold)
        font_turn = QFont("Arial", 22, QFont.DemiBold)

        # Bilgi (sol ortada, soldan biraz içerde)
        self.info_label = QLabel("", self)
        self.info_label.setGeometry(20, screen_height // 2 - 60, 800, 60)  # soldan 20 px, dikey ortalama biraz yukarı
        self.info_label.setFont(font_info)
        self.info_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.info_label.setStyleSheet("color: white;")



        self.turn_label = QLabel("", self)
        self.turn_label.setGeometry(20, screen_height // 2 + 10, 400, 50)  # info_label'ın hemen altında
        self.turn_label.setFont(font_turn)
        self.turn_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.turn_label.setStyleSheet("color: white;")

        # Oyuncu QLabel'larını önce oluştur, sonra resim ata
        self.player = QLabel(self)
        player_image = self.player_image_path if self.player_image_path else "assets/images/player.png"
        self.player.setPixmap(QPixmap(player_image).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.player.move(center_x - 75, center_y + 175)

        self.opponent = QLabel(self)
        opponent_image = self.opponent_image_path if self.opponent_image_path else "assets/images/opponent.png"
        self.opponent.setPixmap(QPixmap(opponent_image).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.opponent.move(center_x - 75, 100)

        # 2. UI Elemanları
        self.shoot_self_btn = QPushButton("Kendine Ateş Et", self)
        self.shoot_self_btn.setGeometry(center_x - 300, screen_height - 150, 150, 40)
        self.shoot_self_btn.clicked.connect(lambda: self.fire(target="self"))

        self.shoot_enemy_btn = QPushButton("Rakibe Ateş Et", self)
        self.shoot_enemy_btn.setGeometry(center_x + 150, screen_height - 150, 150, 40)
        self.shoot_enemy_btn.clicked.connect(lambda: self.fire(target="enemy"))

        # Player 2 butonları (üst kısma)
        self.shoot_self_btn_p2 = QPushButton("Kendine Ateş Et (2P)", self)
        self.shoot_self_btn_p2.setGeometry(center_x - 300, 20, 150, 40)
        self.shoot_self_btn_p2.clicked.connect(lambda: self.fire(target="self", player=1))

        self.shoot_enemy_btn_p2 = QPushButton("Rakibe Ateş Et (2P)", self)
        self.shoot_enemy_btn_p2.setGeometry(center_x + 150, 20, 150, 40)
        self.shoot_enemy_btn_p2.clicked.connect(lambda: self.fire(target="enemy", player=1))

        # Mermiler (küçültülmüş)
        self.shell_labels = []
        shell_start_x = center_x - (6 * 90) // 2 + 10
        for i in range(6):
            lbl = QLabel(self)
            lbl.setPixmap(QPixmap("assets/images/shell_blank.png").scaled(40, 80))
            lbl.setGeometry(shell_start_x + i * 90, center_y - 70, 50, 100)
            self.shell_labels.append(lbl)

        # Item’lar
        self.items = []
        self.items_player1 = []
        self.items_player2 = []

        for i, typ in enumerate(self.item_types):
            img = f"assets/images/item_{typ}.png"

            # Player 1 item
            item1 = Item(self, typ, img, i)
            item1.mousePressEvent = self.create_item_click_handler(i, player=1)
            self.items.append(item1)
            self.items_player1.append(item1)
            item1_x = center_x - ((len(self.item_types) * 90) // 2) + i * 90
            item1_y = screen_height - 80
            item1.move(item1_x, item1_y)

            # Player 2 item
            item2 = Item(self, typ, img, i)
            item2.mousePressEvent = self.create_item_click_handler(i, player=2)
            self.items.append(item2)
            self.items_player2.append(item2)
            item2_x = center_x - ((len(self.item_types) * 90) // 2) + i * 90
            item2_y = 20  # opponent karakterinin hemen üstüne
            item2.move(item2_x, item2_y)

        # Shotgun
        self.shotgun = QLabel(self)
        self.shotgun.setPixmap(
            QPixmap("assets/images/shotgun.png").scaled(300, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.shotgun.setFixedSize(300, 160)
        self.shotgun.setStyleSheet("background: transparent;")
        self.shotgun.move(center_x - 150, center_y - 60)
        self.shotgun_original_pos = (center_x - 150, center_y - 60)

        # Ateş efekti
        self.fire_effect = QLabel(self)
        self.fire_effect.setPixmap(QPixmap("assets/images/fire.png").scaled(60, 60))
        self.fire_effect.setFixedSize(60, 60)
        self.fire_effect.setVisible(False)
        self.fire_effect.setStyleSheet("background: transparent;")
        self.fire_effect.move(center_x, center_y)
        self.update_button_states()

    def create_item_click_handler(self, index, player):
        return lambda e: self.use_item(index, player)

    def update_button_states(self):
        self.shoot_self_btn.setEnabled(self.turn == 0)
        self.shoot_enemy_btn.setEnabled(self.turn == 0)
        self.shoot_self_btn_p2.setEnabled(self.turn == 1)
        self.shoot_enemy_btn_p2.setEnabled(self.turn == 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Oyuncu kalplerini sol alt köşeye yerleştir
        for i, heart in enumerate(self.player_hearts):
            heart.move(20 + i * 45, self.height() - 60)

        # Rakip kalplerini sağ üst köşeye yerleştir
        for i, heart in enumerate(self.opponent_hearts):
            heart.move(self.width() - ((i + 1) * 45), 20)

    def reset_game(self):
        self.shells = [Shell('live')] * 2 + [Shell('blank')] * 4
        random.shuffle(self.shells)
        self.chamber_index = 0
        self.turn = 0
        self.game_over = False
        self.player_health = 1
        self.opponent_health = 1
        self.player_blocked = False
        self.opponent_blocked = False
        self.opponent_shot_rights = 2
        self.info_label.setText("Masaya 6 mermi yerleştirildi.")
        self.turn_label.setText("Senin sıran.")
        self.update_life_labels()



        screen_rect = QApplication.primaryScreen().geometry()
        center_x = screen_rect.width() // 2
        center_y = screen_rect.height() // 2
        self.shotgun.move(center_x - 150, center_y +30)  # Burada  -60 ekle, tıpkı reset_shotgun_position'daki gibi

        self.shotgun.setPixmap(QPixmap("assets/images/shotgun.png").scaled(300, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        for i in range(6):
            self.shell_labels[i].setPixmap(QPixmap("assets/images/shell_blank.png").scaled(60, 120))

        if self.is_first_round:
            for item in self.items:
                item.used = False
                item.setStyleSheet("")
                item.setVisible(True)

        else:
            for item in self.items:
                if item.used:
                    item.setStyleSheet("")
                    item.setVisible(False)
            self.player1_shot_rights += 1
            self.player2_shot_rights += 1
            self.generate_random_item()


    def generate_random_item(self):
        # Her oyuncu için ayrı ayrı işlem yap
        for player_items in [self.items_player1, self.items_player2]:
            # Aktif item tiplerini al (görünür ve kullanılmamış)
            active_types = set(item.item_type for item in player_items if not item.used and item.isVisible())

            # Kullanılmış ama aynı türde olmayan item’ları filtrele
            eligible_items = [item for item in player_items if item.used and item.item_type not in active_types]

            # Eğer 3 item varsa ya da verilecek item kalmadıysa atla
            if len([i for i in player_items if i.isVisible() and not i.used]) >= 3:
                continue
            if not eligible_items:
                continue

            selected_item = random.choice(eligible_items)
            selected_item.used = False
            selected_item.setVisible(True)
            selected_item.setStyleSheet("")


    def update_life_labels(self):
        for i in range(3):
            if i < self.player_lives:
                self.player_hearts[i].setPixmap(
                    QPixmap("assets/images/heart_full.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.player_hearts[i].setPixmap(
                    QPixmap("assets/images/heart_empty.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            if i < self.opponent_lives:
                self.opponent_hearts[i].setPixmap(
                    QPixmap("assets/images/heart_full.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.opponent_hearts[i].setPixmap(
                    QPixmap("assets/images/heart_empty.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def fire(self, target="self", player=None):

        if player is None:
            player = self.turn

        if self.game_over:
            return

        if self.is_two_player:
            if (self.turn == 0 and target not in ["self", "enemy"]) or (
                    self.turn == 1 and target not in ["self", "enemy"]):
                return
        else:
            if player != 0:
                return

        if self.is_first_round:
            self.is_first_round = False

        if target == "enemy":
            if player == 0 and self.player1_shot_rights <= 0:
                self.info_label.setText("1. Oyuncunun rakibe ateş hakkı kalmadı!")
                return
            if player == 1 and self.player2_shot_rights <= 0:
                self.info_label.setText("2. Oyuncunun rakibe ateş hakkı kalmadı!")
                return

        if self.chamber_index >= len(self.shells):
            self.info_label.setText("Mermi kalmadı, yeniden başlıyor.")
            QTimer.singleShot(1500, self.reset_game)
            return

        shell = self.shells[self.chamber_index]
        self.show_shell(self.chamber_index)
        self.chamber_index += 1

        # Ateş efektini zamanla
        QTimer.singleShot(300, lambda: self.trigger_fire_effect(shell))

        # Oyuncu indeksine göre kim kendisi, kim rakip belirle
        if player == 0:
            shooter = "player"
            target_player = "opponent"
        else:
            shooter = "opponent"
            target_player = "player"

        # Rakibe ateş etme durumu
        if target == "enemy":
            if player == 0:
                self.player1_shot_rights -= 1
            else:
                self.player2_shot_rights -= 1

            self.aim_shotgun(target_player)
            if shell.type == "live":
                if target_player == "player":
                    self.player_lives -= 1
                else:
                    self.opponent_lives -= 1
                self.info_label.setText("Rakibi vurdun!")
                if self.player_lives <= 0:
                    if self.is_two_player:
                        self.end_game("2. Oyuncu Kazandı!")
                    else:
                        self.end_game("Kazandın!")
                    return
                elif self.opponent_lives <= 0:
                    if self.is_two_player:
                        self.end_game("1. Oyuncu Kazandı!")
                    else:
                        self.end_game("Kazandın!")
                    return

            else:
                self.info_label.setText("Tık... Boş ateş ettin.")
        else:  # Kendine ateş etme durumu
            self.aim_shotgun(shooter)
            if shooter == "player":
                if self.player_blocked:
                    self.info_label.setText("Korundun! Hasar almadın.")
                    self.player_blocked = False
                elif shell.type == "live":
                    self.player_lives -= 1
                    self.info_label.setText("Kendini vurdun!")
                    if self.player_lives <= 0:
                        if self.is_two_player:
                            self.end_game("2. Oyuncu Kazandı!")
                        else:
                            self.end_game("Kaybettin.")
                        return

                else:
                    self.info_label.setText("Tık... Kendine boş ateş ettin.")
            else:  # shooter == "opponent"
                if self.opponent_blocked:
                    self.info_label.setText("Korundun! Hasar almadın.")
                    self.opponent_blocked = False
                elif shell.type == "live":
                    self.opponent_lives -= 1
                    self.info_label.setText("Kendini vurdun!")
                    if self.opponent_lives <= 0:
                        if self.is_two_player:
                            self.end_game("1. Oyuncu Kazandı!")
                        else:
                            self.end_game("Kaybettin.")
                        return

                else:
                    self.info_label.setText("Tık... Kendine boş ateş ettin.")

        self.update_life_labels()
        if self.is_two_player:
            if self.turn == 0:
                self.turn = 1
                self.turn_label.setText("2. Oyuncunun sırası.")

            else:
                self.turn = 0
                self.turn_label.setText("1. Oyuncunun sırası.")


        self.update_button_states()

    def aim_shotgun(self, target):
        screen_rect = QApplication.primaryScreen().geometry()
        center_x = screen_rect.width() // 2
        center_y = screen_rect.height() // 2

        self.last_target = target
        self.shotgun.setVisible(True)

        width = 300
        height = 150

        original_pixmap = QPixmap("assets/images/shotgun.png").scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        if target == "player":
            rotated_pixmap = original_pixmap.transformed(QTransform().rotate(90), Qt.SmoothTransformation)
        elif target == "opponent":
            rotated_pixmap = original_pixmap.transformed(QTransform().rotate(-90), Qt.SmoothTransformation)
        else:
            rotated_pixmap = original_pixmap

        # QLabel boyutunu pixmap boyutuna göre ayarla
        self.shotgun.setPixmap(rotated_pixmap)
        self.shotgun.setFixedSize(rotated_pixmap.size())

        # Silahın pozisyonunu merkezden pixmap boyutunun yarısı kadar geri çekerek ayarla
        shotgun_x = center_x - rotated_pixmap.width() // 2
        shotgun_y = center_y - rotated_pixmap.height() // 2

        # Target'a göre pozisyon ayarı ve ateş efekti pozisyonu
        if target == "player":
            # Silah aşağı bakıyor, ateş efekti silahın alt ucunda
            self.shotgun.move(shotgun_x, shotgun_y)
            fire_x = shotgun_x + rotated_pixmap.width() // 2 - self.fire_effect.width() // 2
            fire_y = shotgun_y + rotated_pixmap.height() - 10
            self.fire_effect.move(fire_x, fire_y)

        elif target == "opponent":
            # Silah yukarı bakıyor, ateş efekti silahın üst ucunda
            self.shotgun.move(shotgun_x, shotgun_y)
            fire_x = shotgun_x + rotated_pixmap.width() // 2 - self.fire_effect.width() // 2
            fire_y = shotgun_y - self.fire_effect.height() + 10
            self.fire_effect.move(fire_x, fire_y)

        self.shotgun.raise_()
        self.fire_effect.raise_()
        QTimer.singleShot(900, self.reset_shotgun_position)

    def reset_shotgun_position(self):
        screen_rect = QApplication.primaryScreen().geometry()
        center_x = screen_rect.width() // 2
        center_y = screen_rect.height() // 2

        width = 300
        height = 150
        pixmap = QPixmap("assets/images/shotgun.png").scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.shotgun.setPixmap(pixmap)
        self.shotgun.setFixedSize(pixmap.size())
        self.shotgun.move(center_x - pixmap.width() // 2, center_y - pixmap.height() // 2 +80)
        self.shotgun.raise_()

    def trigger_fire_effect(self, shell):
        if shell.type != "live":
            self.empty_player.stop()
            self.empty_player.play()
            return

        self.shotgun_player.stop()  # Ses tekrar oynatılabilsin diye önce durdur
        self.shotgun_player.play()

        # Orijinal pixmap yükle
        original_pixmap = QPixmap("assets/images/fire.png").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Döndürme işlemi
        if self.last_target == "player":
            # +90 derece döndür (silah aşağı baktığında)
            rotated_pixmap = original_pixmap.transformed(QTransform().rotate(90), Qt.SmoothTransformation)
        elif self.last_target == "opponent":
            # -90 derece döndür (silah yukarı baktığında)
            rotated_pixmap = original_pixmap.transformed(QTransform().rotate(-90), Qt.SmoothTransformation)
        else:
            rotated_pixmap = original_pixmap

        self.fire_effect.setPixmap(rotated_pixmap)
        self.fire_effect.setFixedSize(rotated_pixmap.size())

        gun_x = self.shotgun.x()
        gun_y = self.shotgun.y()
        gun_w = self.shotgun.width()
        gun_h = self.shotgun.height()

        effect_w = self.fire_effect.width()
        effect_h = self.fire_effect.height()



        # Pozisyon hesaplama (silahın ucuna göre)
        if self.last_target == "player":
            # Silah aşağı bakıyor → efekt alt ucunda
            effect_x = gun_x + gun_w // 2 - effect_w // 2
            effect_y = gun_y + gun_h - effect_h // 2  # efektin yarısı dışarı taşabilir, test et
        elif self.last_target == "opponent":
            # Silah yukarı bakıyor → efekt üst ucunda
            effect_x = gun_x + gun_w // 2 - effect_w // 2
            effect_y = gun_y - effect_h // 2  # efektin yarısı dışarı taşabilir, test et
        else:
            # Orta pozisyon
            effect_x = gun_x + gun_w // 2 - effect_w // 2
            effect_y = gun_y + gun_h // 2 - effect_h // 2

        self.fire_effect.move(effect_x, effect_y)
        self.fire_effect.setVisible(True)
        self.fire_effect.raise_()
        # Ekle: Ateş efekti 500 ms sonra kaybolsun
        QTimer.singleShot(500, lambda: self.fire_effect.setVisible(False))


    def show_shell(self, idx):
        shell = self.shells[idx]
        img = "assets/images/shell_live.png" if shell.type == "live" else "assets/images/shell_blank.png"
        self.shell_labels[idx].setPixmap(QPixmap(img).scaled(80, 160))

    def use_item(self, index, player):
        if player == 1 and self.turn != 0:
            return
        if player == 2 and self.turn != 1:
            return

        item = self.items_player1[index] if player == 1 else self.items_player2[index]
        if item.used:
            return

        item.mark_used()
        item.setVisible(False)

        if item.item_type == "xray":
            self.show_shell(self.chamber_index)
            self.info_label.setText(f"Player {player} X-ray: Sıradaki mermi gösteriliyor.")

        elif item.item_type == "heal":
            if player == 1 and self.player_lives < 3:
                self.player_lives += 1
                self.info_label.setText("1. Oyuncu canını bir artırdı!")
            elif player == 2 and self.opponent_lives < 3:
                self.opponent_lives += 1
                self.info_label.setText("2. Oyuncu canını bir artırdı!")
            else:
                self.info_label.setText("Can zaten maksimumda!")
            self.update_life_labels()

        elif item.item_type == "block":
            if player == 1:
                self.player_blocked = True
                self.info_label.setText("1. Oyuncu: Koruma aktif.")
            else:
                self.opponent_blocked = True
                self.info_label.setText("2. Oyuncu: Koruma aktif.")

    def end_game(self, msg):
        self.game_over = True
        QMessageBox.information(self, "Oyun Bitti", msg)



def launch_buckshot_game_2player(player_image_path=None, opponent_image_path=None):
    app = QApplication(sys.argv)
    window = GameWindow(player_image_path=player_image_path, opponent_image_path=opponent_image_path)
    window.showFullScreen()
    sys.exit(app.exec_())



