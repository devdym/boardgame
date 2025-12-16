from os import listdir
from os.path import isfile, join

import pygame

from lib.outliner import Outliner

WIDTH, HEIGHT = 1280, 720
PLAYER_VEL = 5


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    outliner = Outliner()

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            if image == "outlined.png":
                sprites.append(
                    outliner.outline_surface(
                        pygame.transform.scale2x(surface),
                        color="red",
                        outline_only=False,
                    )
                )
            else:
                sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "_right")] = sprites
            all_sprites[image.replace(".png", "_up")] = sprites
            all_sprites[image.replace(".png", "_down")] = sprites
            all_sprites[image.replace(".png", "_left")] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)

    return pygame.transform.scale2x(surface)


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def draw(window, background, bg_image, objects, pl1, pl2, pl1_dash, pl2_dash):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window)

    pl1.draw(window, 0)
    pl2.draw(window, 0)

    for pl in pl1_dash:
        window.blit(pl[0], pl[1])

    for pl in pl2_dash:
        window.blit(pl[0], pl[1])

    pygame.display.update()


def handle_vertical_collision(hero, objects, dx, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(hero, obj):
            if dy > 0:
                hero.rect.bottom = obj.rect.top
                hero.hit_head()
                # hero.landed()
            elif dy < 0:
                hero.rect.top = obj.rect.bottom
                hero.hit_head()
            if dx > 0:
                hero.rect.right = obj.rect.left
                hero.hit_head()
            elif dx < 0:
                hero.rect.left = obj.rect.right
                hero.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(hero, player1, player2, active_pl, dx, dy):
    hero.move(dx, dy, 0)
    hero.update()
    collided_object = None

    if active_pl == 2:
        for obj in player1.heroes_list:
            if pygame.sprite.collide_mask(hero, obj):
                collided_object = obj
                obj.move(10, 10, 10)
                obj.make_hit()
                break

    if active_pl == 1:
        for obj in player2.heroes_list:
            if pygame.sprite.collide_mask(hero, obj):
                collided_object = obj
                obj.move(10, 10, 10)
                obj.make_hit()
                break
    hero.move(-dx, dy, 500)
    hero.update()
    return collided_object


# def handle_move(active_player, active_hero, player1, player2, objects, steps_player1):
#     if active_player == 1:
#         play_heroes = player1.heroes_list
#     else:
#         play_heroes = player2.heroes_list

#     hero = play_heroes[active_hero]

#     keys = pygame.key.get_pressed()

#     hero.x_vel = 0
#     hero.y_vel = 0
#     collide_left = collide(hero, player1, player2, -PLAYER_VEL * 2, 0)
#     collide_right = collide(hero, player1, player2, PLAYER_VEL * 2, 0)

#     # change hero of same player
#     if keys[pygame.K_TAB]:
#         play_heroes[active_hero].selected = False

#         if active_hero < len(play_heroes) - 1:
#             active_hero = active_hero + 1
#         else:
#             active_hero = 0

#     # change player and activate first hero
#     if keys[pygame.K_n]:
#         play_heroes[active_hero].selected = False

#         active_hero = 0
#         active_player = active_player + 1

#         if active_player >= 3:
#             active_player = 1
#         else:
#             active_player = 2

#         if active_player == 1:
#             play_heroes = player1.heroes_list

#         else:
#             play_heroes = player2.heroes_list

#     play_heroes[active_hero].selected = False

#     if active_player == 1:
#         play_heroes = player1.heroes_list
#     if active_player == 2:
#         play_heroes = player2.heroes_list

#     play_heroes[active_hero].selected = True

#     print(f"active player: {active_player}")
#     print(f"active hero: {active_hero}")

#     if keys[pygame.K_LEFT] and not collide_left:
#         hero.move_left(PLAYER_VEL)
#         steps_player1 = steps_player1 + 1
#     if keys[pygame.K_RIGHT] and not collide_right:
#         hero.move_right(PLAYER_VEL)
#         steps_player1 = steps_player1 + 1
#     if keys[pygame.K_UP]:
#         hero.move_up(PLAYER_VEL)
#         steps_player1 = steps_player1 + 1
#     if keys[pygame.K_DOWN]:
#         hero.move_down(PLAYER_VEL)
#         steps_player1 = steps_player1 + 1

#     # print(f"steps_pl1 {steps_player1}")

#     vertical_collide = handle_vertical_collision(hero, objects, hero.y_vel)
#     to_check = [
#         collide_left,
#         collide_right,
#         *vertical_collide,
#     ]

#     for obj in to_check:
#         if obj and obj.name == "block":
#             hero.make_hit()
