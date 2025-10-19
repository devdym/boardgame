from lib.hero import Hero

class Player():
    def __init__(self, steps, location, heroes, direction, FPS, window):
        super().__init__()
        self.steps = steps
        self.heroes_list = []
        self.window = window
        self.location = location
        step = 100
        self.direction = direction

        for hero in heroes:
            h = Hero(location, step, 50, 50, hero, self.direction, False)
            step = step + 150
            self.heroes_list.append(h)
            h.loop(FPS)
            h.draw(window, 0)
    
    def draw(self, window, offset_x):
        for hero in self.heroes_list:
            hero.draw(self.window, offset_x)