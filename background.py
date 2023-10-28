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
        self.image = load_image('ai_keeper-removebg-preview.png')

    def update(self):
        self.frame = (self.frame + 1) % 2


    def draw(self):
        self.image.clip_draw(self.frame * 1, 0, 20, 40, self.x, self.y, 80, 200)


class Ai_Kicker:
    def __init__(self):
        self.x, self.y = 300, 0
        self.frame = 0
        self.image = load_image('ai_kicker-removebg-preview.png')

    def update(self):
        self.frame = (self.frame + 1) % 2


    def draw(self):
        self.image.clip_draw(self.frame * 1, 0, 30, 80, self.x, self.y, 100, 200)



class Ball:
    def __init__(self):
        self.x, self.y = 400, 20
        self.frame = 0
        self.image = load_image('ball21x21.png')

    def update(self):
        self.frame = (self.frame + 1) % 2


    def draw(self):
        self.image.clip_draw(self.frame * 1, 0, 80, 80, self.x, self.y,40,40)


def handle_events():
    pass


open_canvas()


def reset_world():
    global running
    global background
    global ai_keeper
    global ai_kicker
    global ball

    running = True
    background = Background()
    ai_keeper = Ai_Keeper()
    ai_kicker = Ai_Kicker()
    ball = Ball()

def update_world():
    background.update()
    ai_keeper.update()
    ai_kicker.update()
    ball.update()
    pass


def render_world():
    clear_canvas()
    background.draw()
    ai_keeper.draw()
    ai_kicker.draw()
    ball.draw()
    update_canvas()


open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
close_canvas()
