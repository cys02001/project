from pico2d import load_image


class Ground:
    def __init__(self):
        self.image = load_image('ground.png')
        global gauge_bar_image
        gauge_bar_image = load_image('gauge_bar.png')
    def draw(self):
        self.image.draw(400, 300, 800, 600)
        gauge_bar_image.draw(400,100)
    def update(self):
        pass
