from pico2d import *


class Background:
    def __init__(self):
        self.image = load_image('ground.png')

    def draw(self):
        self.image.draw(400, 300, 800, 600)

    def update(self): pass


def handle_events():
    pass


open_canvas()


def reset_world():
    global running
    global background

    running = True
    background = Background()


def update_world():
    background.update()
    pass


def render_world():
    clear_canvas()
    background.draw()
    update_canvas()


open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
close_canvas()
