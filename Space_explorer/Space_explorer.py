from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from random import *
from pygame import *
import json

mixer.init()
font.init()


app = QApplication([])

window_menu = QWidget()
window_menu.resize(500, 450)
window_menu.setWindowTitle("Space explorer")

btn_play = QPushButton("Грати")
btn_exit = QPushButton("Вийти")
btn_settings = QPushButton("Налаштування")

version_label = QLabel("Version 2.0 beta 2")

menu_layout = QVBoxLayout()
menu_layout.addStretch(1)
menu_layout.addWidget(btn_play)
menu_layout.addWidget(btn_settings)
menu_layout.addWidget(btn_exit)
menu_layout.addStretch(1)
menu_layout.addWidget(version_label,  alignment=Qt.AlignRight)

explorer = transform.scale(image.load("player.png"), (50, 50))
meteorit_img = transform.scale(image.load("meteor.png"), (50, 50))
gan_shot = transform.scale(image.load("gan.png"), (50, 50))
background = transform.scale(image.load("fon.jpg"), (500, 450))
shield_img = transform.scale(image.load("shield.png"), (50, 50))
shield_icon = transform.scale(image.load("shield.png"), (50, 50))
display.set_caption("Space explorer")

game = True
finish = False

meteorits = []
active_meteorits = []
clock = time.Clock()
speed = 5
score = 0
meteorit_spawn_time = 2000 
shield = 0 
shield_token = 0
shield_x = 0
shield_y = 0
active_shields = 0

def play():
    global game

    last_shot_time = 0
    last_meteorit_spawn_time = 0

    window_menu.close()

    x = 225
    y = 400

    shots = []
    shields = []

    window_game = display.set_mode((500, 450))

    back = (250, 0, 0)
    window_game.fill(back)

    mixer.music.load("music.ogg")
    mixer.music.play(5)

    score_font = font.Font("stareagle2.ttf", 20)

    laser_shot = mixer.Sound("laser_shot.ogg")
    shield_sound = mixer.Sound("shield.ogg")


    def create_meteorit():
        meteorit_x = randint(0, 450)  
        meteorit_speed = 2
        meteorits.append([meteorit_x, 0, meteorit_speed])
        active_meteorits.append(len(meteorits) - 1) 


    def draw_meteorits():
        for meteorit in meteorits:
            meteorit_x, meteorit_y, = meteorit
            window_game.blit(meteorit_img, (meteorit_x, meteorit_y)) 

    def death():
        global finish
        global shield

        if shield == 0:
            game_over_m = mixer.Sound("GAME_OVER.ogg")

            game_over_font = font.Font("Martirio_Digital.ttf", 70)
            death_font = font.Font("Martirio_Digital.ttf", 70)

            game_over = game_over_font.render("GAME OVER", True, (0, 0, 0))
            death_label = death_font.render("You die", True, (0, 0, 0))

            window_game.fill((255, 0, 0)) 
            window_game.blit(game_over, (60, 150))
            window_game.blit(death_label, (110, 240))

            mixer.music.stop()
            game_over_m.play()

            finish = True

        elif shield >= 1:
            shield_sound.play()
            shield = 0

    def check_collision():
        global game
        global meteorits
        global active_meteorits
        global score
        global shield
        global shield_token
        global shield_x
        global shield_rect
        global active_shields

        meteorits_to_remove = []
        shots_to_remove = []

        explorer_rect = Rect(x, y, 50, 50)
        shield_rect = Rect(shield_x, shield_y, 50, 50)

        for meteorit in meteorits:
            meteorit_rect = Rect(meteorit[0], meteorit[1], 50, 50)
            if meteorit_rect.colliderect(explorer_rect):
                meteorits.remove(meteorit)
                death()
                return
            elif shield_rect.colliderect(explorer_rect):
                shield += 1

            for shot in shots:
                shot_rect = Rect(shot[0], shot[1], 50, 50)
                if meteorit_rect.colliderect(shot_rect):
                    meteorits_to_remove.append(meteorit)
                    shots_to_remove.append(shot)

        for meteorit in meteorits_to_remove:
            meteorits.remove(meteorit)
            #shield_token = randint(1,20)
            score += 2
            shield_token += 15
            active_shields += 1
            if active_shields <= 1:
                print(shield_token)
                shield_x = randint(0, 450)

        for shot in shots_to_remove:
            shots.remove(shot)

    while game:
        global score
        global shield_img

        window_game.blit(background, (0, 0))
        window_game.blit(explorer, (x, y))

        score_text = score_font.render("SCORE  "+str(score), True, (0, 255, 0))
        window_game.blit(score_text, (5,10))

        keys_pressed = key.get_pressed()

        if keys_pressed[K_a] and x > 5:
            x -= speed

        if keys_pressed[K_d] and x < 450:
            x += speed

        for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    current_time = time.get_ticks()
                    if current_time - last_shot_time >= 700:
                        laser_shot.play()
                        shots.append([x + 15, y])
                        last_shot_time = current_time
        if not finish:

            check_collision()

            for shot in shots:
                shot[1] -= 10

            for meteorit in meteorits:
                meteorit[1] += meteorit[2]
                if meteorit[1] > 450:
                    meteorits.remove(meteorit)
                    score -= 3

            draw_meteorits()

            for shot in shots:
                window_game.blit(gan_shot, (shot[0], shot[1]))

            shots = [shot for shot in shots if shot[1] > 0]

            current_time = time.get_ticks()
            if current_time - last_meteorit_spawn_time >= meteorit_spawn_time:
                create_meteorit()
                last_meteorit_spawn_time = current_time

            if score <= -10:
                death()

            if shield_token == 15:
                shields.append(shield_img)

            if shield_img in shields:
                global shield_y

                window_game.blit(shield_img, (shield_x, shield_y))

            if active_shields >= 1:
                if shield_y <= 200:
                    shield_y += 2
                elif shield_y >= 200:
                    shields.remove(shield_img)

            display.update()
            clock.tick(120)

def exit():
    app.quit()

def menu():
    window_menu.show()

btn_play.clicked.connect(play)
btn_exit.clicked.connect(exit)

window_menu.setLayout(menu_layout)
window_menu.show()

app.exec_()