from pico2d import *


class Background:
    def __init__(self):
        self.image = load_image('ground.png')

    def draw(self):
        self.image.draw(400, 300, 800, 600)

    def update(self): pass


class Ai_Keeper:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.image = load_image('ai_keeper.png')

    def update(self):
        self.frame = (self.frame + 1) % 2


    def draw(self):
        self.image.clip_draw(self.frame * 50, 0, 100, 100, self.x, self.y)


def handle_events():
    pass


open_canvas()


def reset_world():
    global running
    global background
    global ai_keeper

    running = True
    background = Background()
    ai_keeper = Ai_Keeper()


def update_world():
    background.update()
    ai_keeper.update()
    pass


def render_world():
    clear_canvas()
    background.draw()
    ai_keeper.draw()
    update_canvas()


open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
close_canvas()
