import pygame


class HealthBar:
    def __init__(self, x, y, w, h, max_hp):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def loop(self, surface):
        # ratio = self.hp / self.max_hp
        self.rect = pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        # pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))
