from lib.hero import Hero


class Player:
    def __init__(self, steps, location, heroes, direction, player, FPS, window):
        super().__init__()
        self.steps = steps
        self.heroes_list = []
        self.window = window
        self.location = location
        # step = 100
        self.direction = direction
        self.player = player

        for hero in heroes:
            h = Hero(
                self.location,
                self.steps,
                50,
                50,
                hero,
                self.player,
                self.direction,
                False,
            )
            self.steps = self.steps + 150
            self.heroes_list.append(h)
            h.loop(FPS)
            h.draw(window, 0)

    def draw(self, window, offset_x):
        for hero in self.heroes_list:
            hero.draw(self.window, offset_x)
