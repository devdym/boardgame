from os import listdir
from os.path import isfile, join

import pygame

WIDTH, HEIGHT = 1000, 800
PLAYER_VEL = 5


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "_right")] = sprites
            all_sprites[image.replace(".png", "_up")] = sprites
            all_sprites[image.replace(".png", "_down")] = sprites
            all_sprites[image.replace(".png", "_left")] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)

    return pygame.transform.scale2x(surface)


def draw(window, background, bg_image, player, objects):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window)

    player.draw(window)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

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


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    player.y_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL, 0)
    collide_right = collide(player, objects, PLAYER_VEL, 0)
    # collide_up = collide(player, objects, PLAYER_VEL * 2, -PLAYER_VEL * 2)
    # collide_down = collide(player, objects, PLAYER_VEL * 2, -PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
    if keys[pygame.K_UP]:
        player.move_up(PLAYER_VEL)
    if keys[pygame.K_DOWN]:
        player.move_down(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)

    to_check = [collide_left, collide_right, *vertical_collide]
    # to_check = [*vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()
