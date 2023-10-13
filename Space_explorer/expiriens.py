from random import *
from pygame import *

window_menu = display.set_mode((500, 450))

explorer = transform.scale(image.load("player.png"), (50, 50))
meteorit_img = transform.scale(image.load("meteor.png"), (50, 50))
gan_shot = transform.scale(image.load("gan.png"), (50, 50))
background = transform.scale(image.load("fon.jpg"), (500, 450))
fon = transform.scale(image.load("preview.jpg"), (500, 450))
btn_play = transform.scale(image.load("play.png"), (450, 320))
btn_setting = transform.scale(image.load("setting.png"), (450, 320))
btn_exit = transform.scale(image.load("exit.png"), (450, 320))

display.set_caption("Space Explorer")

menu = True
game = False

font.init()
font = font.SysFont(None, 36)

def draw_menu():
    window_menu.blit(fon, (0, 0))

    play_rect = btn_play.get_rect(center=(250, 150))
    window_menu.blit(btn_play, play_rect)

    setting_rect = btn_setting.get_rect(center=(250, 250))
    window_menu.blit(btn_setting, setting_rect)

    exit_rect = btn_exit.get_rect(center=(250, 350))
    window_menu.blit(btn_exit, exit_rect)

    play_text = font.render("Play", True, (255, 255, 255))
    window_menu.blit(play_text, play_text.get_rect(center=play_rect.center))

    setting_text = font.render("Setting", True, (255, 255, 255))
    window_menu.blit(setting_text, setting_text.get_rect(center=setting_rect.center))

    exit_text = font.render("Exit", True, (255, 255, 255))
    window_menu.blit(exit_text, exit_text.get_rect(center=exit_rect.center))

    display.update()

def check_menu_buttons(pos):
    play_rect = btn_play.get_rect(center=(250, 150))
    setting_rect = btn_setting.get_rect(center=(250, 250))
    exit_rect = btn_exit.get_rect(center=(250, 350))

    if play_rect.collidepoint(pos):
        return "play"
    elif setting_rect.collidepoint(pos):
        return "setting"
    elif exit_rect.collidepoint(pos):
        return "exit"
    else:
        return None

while menu:
    draw_menu()

    for e in event.get():
        if e.type == QUIT:
            menu = False
            break
        elif e.type == MOUSEBUTTONDOWN:
            button_pressed = check_menu_buttons(mouse.get_pos())
            if button_pressed == "play":
                game = True
                menu = False
                break
            elif button_pressed == "exit":
                menu = False
                break

if game:
    x = 225
    y = 400

    shots = []

    window_game = display.set_mode((500, 450))
    display.set_caption("Space explorer")

    meteorits = []
    clock = time.Clock()
    speed = 5
    meteorit_spawn_time = 2000

    def create_meteorit():
        meteorit_x = randint(0, 450)  
        meteorit_speed = 2
        meteorits.append([meteorit_x, 0, meteorit_speed])

    def draw_meteorits():
        for meteorit in meteorits:
            meteorit_x, meteorit_y, _ = meteorit
            window_game.blit(meteorit_img, (meteorit_x, meteorit_y))

    def check_collision():
        global game
        global meteorits

        meteorits_to_remove = []
        shots_to_remove = []

        explorer_rect = Rect(x, y, 50, 50)

        for meteorit in meteorits:
            meteorit_rect = Rect(meteorit[0], meteorit[1], 50, 50)
            if meteorit_rect.colliderect(explorer_rect):
                game = False
                return

            for shot in shots:
                shot_rect = Rect(shot[0], shot[1], 50, 50)
                if meteorit_rect.colliderect(shot_rect):
                    meteorits_to_remove.append(meteorit)
                    shots_to_remove.append(shot)

        for meteorit in meteorits_to_remove:
            meteorits.remove(meteorit)

        for shot in shots_to_remove:
            shots.remove(shot)

    while game:
        window_game.blit(background, (0, 0))
        window_game.blit(explorer, (x, y))

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
                        shots.append([x + 15, y])
                        last_shot_time = current_time

        check_collision()

        for shot in shots:
            shot[1] -= 10

        for meteorit in meteorits:
            meteorit[1] += meteorit[2]
            if meteorit[1] > 450:
                meteorits.remove(meteorit)

        draw_meteorits()

        for shot in shots:
            window_game.blit(gan_shot, (shot[0], shot[1]))

        shots = [shot for shot in shots if shot[1] > 0]

        current_time = time.get_ticks()
        if current_time - last_meteorit_spawn_time >= meteorit_spawn_time:
            create_meteorit()
            last_meteorit_spawn_time = current_time

        display.update()
        clock.tick(120)
