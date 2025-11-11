import pygame, sys
from lib.fire import Fire
from lib.load import get_background
from lib.block import Block
from lib.player import Player
from button import Button

pygame.init()
pygame.display.set_caption("BoardGame")

WIDTH, HEIGHT = 1280, 720
FPS = 90
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def draw(window, background, bg_image, objects, pl1, pl2):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window)

    # for player in players.heroes:
    #     player.draw(window, offset_x)

    pl1.draw(window, 0)
    pl2.draw(window, 0)

    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
            elif dy < 0:
                player.rect.top = obj.rect.bottom

            collided_objects.append(obj)

    return collided_objects

def collide(player, objects, dx, dy):
    player.move(dx, dy, 500)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, dy, 500)
    player.update()
    return collided_object 

def handle_move(active_player, active_hero, player1, player2, objects, steps_player1):
    if active_player == 1:
        play_heroes = player1.heroes_list
    else:
        play_heroes = player2.heroes_list

    hero = play_heroes[active_hero]
    
    keys = pygame.key.get_pressed()

    hero.x_vel = 0
    hero.y_vel = 0
    collide_left = collide(hero, objects, -PLAYER_VEL * 2, PLAYER_VEL * 2)
    collide_right = collide(hero, objects, PLAYER_VEL * 2, PLAYER_VEL * 2)
    collide_up = collide(hero, objects, PLAYER_VEL * 2, -PLAYER_VEL * 2)
    collide_down = collide(hero, objects, -PLAYER_VEL * 2, -PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        hero.move_left(PLAYER_VEL)
        steps_player1 = steps_player1 + 1
    if keys[pygame.K_RIGHT] and not collide_right:
        hero.move_right(PLAYER_VEL)
        steps_player1 = steps_player1 + 1
    if keys[pygame.K_UP] and not collide_up:
        hero.move_up(PLAYER_VEL)
        steps_player1 = steps_player1 + 1
    if keys[pygame.K_DOWN] and not collide_down:
        hero.move_down(PLAYER_VEL)
        steps_player1 = steps_player1 + 1
    
    print(f'steps_pl1 {steps_player1}')

    vertical_collide = handle_vertical_collision(hero, objects, hero.y_vel)

    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            hero.make_hit() 

def two_players():
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96

    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    # floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [ Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]

    player1 = Player(100, 100, ["MaskDude", "NinjaFrog"], "right", FPS, window)
    player1_steps = 100

    player2 = Player(100, 400, ["VirtualGuy", "PinkMan"], "left", FPS, window)
    player2_steps = 100

    active_player = 1
    active_hero = 0
    
    

    run = True
    while run:
        clock.tick(FPS)
        player1.heroes_list[0].loop(FPS)
        player1.heroes_list[1].loop(FPS)
        player2.heroes_list[0].loop(FPS)
        player2.heroes_list[1].loop(FPS)
        fire.loop()

        # handle_move(active_player, active_hero, player1, player2, objects, player1_steps)
        draw(window, background, bg_image, objects, player1, player2)

        if active_player == 1:
            play_heroes = player1.heroes_list
        else:
            play_heroes = player2.heroes_list

        play_heroes[active_hero].selected = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                hero = play_heroes[active_hero]
                hero.x_vel = 0
                hero.y_vel = 0
                collide_left = collide(hero, objects, -PLAYER_VEL * 2, PLAYER_VEL * 2)
                collide_right = collide(hero, objects, PLAYER_VEL * 2, PLAYER_VEL * 2)
                collide_up = collide(hero, objects, PLAYER_VEL * 2, -PLAYER_VEL * 2)
                collide_down = collide(hero, objects, -PLAYER_VEL * 2, -PLAYER_VEL * 2)

                # change hero of same player
                if event.key == pygame.K_TAB:
                    play_heroes[active_hero].selected = False

                    if active_hero < len(play_heroes)-1:
                        active_hero = active_hero + 1
                    else:
                        active_hero = 0

                # change player and activate first hero
                if event.key == pygame.K_n:
                    play_heroes[active_hero].selected = False

                    active_hero = 0
                    active_player = active_player + 1
                    
                    if active_player >=3:
                        active_player = 1
                    else:
                        active_player = 2

                    if active_player == 1:
                        play_heroes = player1.heroes_list

                    else:
                        play_heroes = player2.heroes_list
                    
                play_heroes[active_hero].selected = False
                
                if active_player == 1:
                    play_heroes = player1.heroes_list
                if active_player == 2:
                    play_heroes = player2.heroes_list
                
                play_heroes[active_hero].selected = True
                
                print(f'active player: {active_player}')
                print(f'active hero: {active_hero}')

                if event.key == pygame.K_LEFT and not collide_left:
                    hero.move_left(PLAYER_VEL)
                    player1_steps = player1_steps + 1
                if event.key == pygame.K_RIGHT and not collide_right:
                    hero.move_right(PLAYER_VEL)
                    player1_steps = player1_steps + 1
                if event.key == pygame.K_UP and not collide_up:
                    hero.move_up(PLAYER_VEL)
                    player1_steps = player1_steps + 1
                if event.key == pygame.K_DOWN and not collide_down:
                    hero.move_down(PLAYER_VEL)
                    player1_steps = player1_steps + 1

                print(f'player1_steps: {player1_steps}')

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and player.jump_count < 2:
            #         player.jump()

def main(window):
    while True:
        window.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MY GAME", True, "#b68f40")

        PL1_TEXT = get_font(30).render("Player 1", True, "#404eb6")
        PL1_Rect = PL1_TEXT.get_rect()
        PL1_Rect.center = (200, 20)

        PL1_CH1 = get_font(20).render("Knight", True, "#17e32f")
        PL1_CH1_Rect = PL1_CH1.get_rect()
        PL1_CH1_Rect.center = (200, 100)
        PL1_CH2 = get_font(20).render("Princess", True, "#ffffff")
        PL1_CH2_Rect = PL1_CH2.get_rect()
        PL1_CH2_Rect.center = (200, 160)
        PL1_CH3 = get_font(20).render("Alchemist", True, "#17e32f")
        PL1_CH3_Rect = PL1_CH3.get_rect()
        PL1_CH3_Rect.center = (200, 210)
        PL1_CH4 = get_font(20).render("Puss", True, "#17e32f")
        PL1_CH4_Rect = PL1_CH4.get_rect()
        PL1_CH4_Rect.center = (200, 270)
        PL1_CH5 = get_font(20).render("Bush", True, "#ffffff")
        PL1_CH5_Rect = PL1_CH5.get_rect()
        PL1_CH5_Rect.center = (200, 330)

        PL2_TEXT = get_font(30).render("Player 2", True, "#e04b1e")
        PL2_Rect = PL2_TEXT.get_rect()
        PL2_Rect.center = (1000, 20)

        PL2_CH1 = get_font(20).render("Knight", True, "#17e32f")
        PL2_CH1_Rect = PL2_CH1.get_rect()
        PL2_CH1_Rect.center = (1000, 100)
        PL2_CH2 = get_font(20).render("Princess", True, "#ffffff")
        PL2_CH2_Rect = PL2_CH2.get_rect()
        PL2_CH2_Rect.center = (1000, 160)
        PL2_CH3 = get_font(20).render("Alchemist", True, "#ffffff")
        PL2_CH3_Rect = PL2_CH3.get_rect()
        PL2_CH3_Rect.center = (1000, 210)
        PL2_CH4 = get_font(20).render("Puss", True, "#17e32f")
        PL2_CH4_Rect = PL2_CH4.get_rect()
        PL2_CH4_Rect.center = (1000, 270)
        PL2_CH5 = get_font(20).render("Bush", True, "#17e32f")
        PL2_CH5_Rect = PL2_CH5.get_rect()
        PL2_CH5_Rect.center = (1000, 330)

        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))


        START_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(WIDTH//2, HEIGHT//2), 
                            text_input="START", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(WIDTH//2, (HEIGHT//2)+110), 
                            text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        window.blit(PL1_TEXT, PL1_Rect)
        window.blit(PL1_CH1, PL1_CH1_Rect)
        window.blit(PL1_CH2, PL1_CH2_Rect)
        window.blit(PL1_CH3, PL1_CH3_Rect)
        window.blit(PL1_CH4, PL1_CH4_Rect)
        window.blit(PL1_CH5, PL1_CH5_Rect)
        window.blit(PL2_TEXT, PL2_Rect)
        window.blit(PL2_CH1, PL2_CH1_Rect)
        window.blit(PL2_CH2, PL2_CH2_Rect)
        window.blit(PL2_CH3, PL2_CH3_Rect)
        window.blit(PL2_CH4, PL2_CH4_Rect)
        window.blit(PL2_CH5, PL2_CH5_Rect)
        

        for button in [START_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                    two_players()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)
