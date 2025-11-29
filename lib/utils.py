from os import listdir
from os.path import isfile, join

import pygame

from lib.outliner import Outliner

WIDTH, HEIGHT = 1280, 720


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


def handle_collision(player, objects, dx, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
            elif dy < 0:
                player.rect.top = obj.rect.bottom
            elif dx > 0:
                player.rect.right = obj.rect.left
            elif dx < 0:
                player.rect.left = obj.rect.right

            collided_objects.append(obj)

    return collided_objects


def collide(hero, player1, player2, dx, dy):
    hero.move(dx, dy, 500)
    hero.update()
    collided_object = None
    for obj in player1.heroes_list:
        if pygame.sprite.collide_mask(hero, obj):
            collided_object = obj
            break

    for obj in player2.heroes_list:
        if pygame.sprite.collide_mask(hero, obj):
            collided_object = obj
            break

    hero.move(-dx, dy, 500)
    hero.update()
    return collided_object
