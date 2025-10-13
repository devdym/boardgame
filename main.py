import pygame
from lib.fire import Fire
from lib.load import get_background
from lib.block import Block
from lib.hero import Hero
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
    player.move(dx, dy)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, dy)
    player.update()
    return collided_object 

def handle_move(player, objects, steps_player1):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    player.y_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2, PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2, PLAYER_VEL * 2)
    collide_up = collide(player, objects, PLAYER_VEL * 2, -PLAYER_VEL * 2)
    collide_down = collide(player, objects, -PLAYER_VEL * 2, -PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
        steps_player1 = steps_player1 + 1
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
        steps_player1 = steps_player1 + 1
    if keys[pygame.K_UP] and not collide_up:
        player.move_up(PLAYER_VEL)
        steps_player1 = steps_player1 + 1
    if keys[pygame.K_DOWN] and not collide_down:
        player.move_down(PLAYER_VEL)
        steps_player1 = steps_player1 + 1
    
    print(f'steps_pl1 {steps_player1}')

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)

    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit() 

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96

    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]

    # hero1 = Hero(100, 100, 50, 50, "MaskDude", False)
    # hero2 = Hero(100, 150, 50, 50, "NinjaFrog", False)
    # hero3 = Hero(50, 100, 50, 50, "VirtualGuy", False)
    # hero4 = Hero(200, 200, 50, 50, "MaskDude", False)

    player1 = Player(100, ["MaskDude", "NinjaFrog"], FPS, window)
    player2 = Player(100, ["VirtualGuy", "MaskDude"], FPS, window)

    # heroes = [hero1, hero2, hero3, hero4]
    # heroes[active_hero].selected = True

    # scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        # hero1.loop(FPS)
        # hero2.loop(FPS)
        # hero3.loop(FPS)
        # hero4.loop(FPS)
        fire.loop()

        # handle_move(hero1, objects, steps_player1)
        draw(window, background, bg_image, objects, player1, player2)

        # if ((hero1.rect.right - offset_x >= WIDTH - scroll_area_width) and hero1.x_vel > 0) or (
        #     (hero1.rect.left - offset_x <= scroll_area_width) and hero1.x_vel < 0):
        #     offset_x += hero1.x_vel

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_TAB:
            #         heroes[active_hero].selected = False

            #         if active_hero < len(heroes)-1:
            #             active_hero = active_hero + 1
            #         else:
            #             active_hero = 0
                    
            #         heroes[active_hero].selected = True

                
            #         print(f'active_hero {active_hero}')

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and player.jump_count < 2:
            #         player.jump()
        

        # for event in pygame.event.get():
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if event.button == 1:
        #             for num, box in enumerate(players):
        #                 if box.collidepoint(event.pos):
        #                     active_hero = num
        #                     print(active_hero)
            
        #     if event.type == pygame.MOUSEBUTTONUP:
        #         if event.button == 1:
        #             active_hero = None



    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)
