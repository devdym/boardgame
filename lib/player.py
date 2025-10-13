from lib.hero import Hero

class Player():
    def __init__(self, steps, heroes, FPS, window):
        super().__init__()
        self.steps = steps
        self.heroes_list = []
        self.window = window


        for hero in heroes:
            h = Hero(100, 100, 50, 50, hero, False)
            self.heroes_list.append(h)
            h.loop(FPS)
            h.draw(window, 0)
    
    def draw(self, window, offset_x):
        for hero in self.heroes_list:
            hero.draw(self.window, offset_x)