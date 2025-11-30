import pygame

from lib.block import Block

# from lib.fire import Fire
from lib.utils import draw, get_background, handle_move, load_sprite_sheets

pygame.init()
pygame.display.set_caption("Sandbox")

WIDTH, HEIGHT = 1000, 800
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    # GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.hit = False
        self.hit_count = 0
        # self.fall_count = 0
        # self.jump_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def move_down(self, vel):
        self.y_vel = vel
        if self.direction != "down":
            self.direction = "down"
            self.animation_count = 0

    def move_up(self, vel):
        self.y_vel = -vel
        if self.direction != "up":
            self.direction = "up"
            self.animation_count = 0

    def loop(self, fps):
        # self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        # self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        # if self.y_vel < 0:
        #     if self.jump_count == 1:
        #         sprite_sheet = "jump"
        #     elif self.jump_count == 2:
        #         sprite_sheet = "double_jump"
        # elif self.y_vel > self.GRAVITY * 2:
        #     sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"
        elif self.y_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        # self.sprite = self.SPRITES["idle_" + self.direction][0]
        win.blit(self.sprite, (self.rect.x, self.rect.y))

    # def jump(self):
    # self.y_vel = -self.GRAVITY * 8
    #     self.animation_count = 0
    #     self.jump_count += 1
    #     if self.jump_count == 1:
    #         self.fall_count = 0

    def landed(self):
        # self.fall_count = 0
        self.y_vel = 0
        # self.jump_count = 0

    def hit_head(self):
        # self.count = 0
        self.y_vel *= -1


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96

    player = Player(100, 100, 50, 50)
    # fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    # fire.on()
    # floor = [
    #     Block(i * block_size, HEIGHT - block_size, block_size)
    #     for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)
    # ]
    objects = [
        # *floor,
        Block(0, HEIGHT - block_size * 2, block_size),
        Block(block_size * 3, HEIGHT - block_size * 4, block_size),
        # fire,
    ]

    # offset_x = 0
    # scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and player.jump_count < 2:
            #         player.jump()

        player.loop(FPS)
        # fire.loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects)

        # if (
        #     (player.rect.right - offset_x >= WIDTH - scroll_area_width)
        #     and player.x_vel > 0
        # ) or ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
        #     offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
