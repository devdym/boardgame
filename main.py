import pygame
from lib.fire import Fire
from lib.load import get_background
from lib.block import Block
from lib.player import Player


pygame.init()
pygame.display.set_caption("BoardGame")

WIDTH, HEIGHT = 1000, 800
FPS = 90
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

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

def main(window):
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

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)
