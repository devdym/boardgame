import pygame

from lib.object import Object
from lib.utils import load_sprite_sheets


class Flag(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, "flag")
        self.flag = load_sprite_sheets("Traps", "Red", width, height, False)
        self.image = self.flag["off"][0]
        if color == "Blue":
            self.image = pygame.transform.hsl(self.image, 0.5, 0.8, 0.6)
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.flag[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
