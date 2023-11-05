from pico2d import *
from background import Background
from keeper import Keeper


# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            keeper.handle_event(event)


def reset_world():
    global running
    global background
    global team
    global world
    global keeper

    running = True
    world = []

    background = Background()
    world.append(background)

    keeper = Keeper()
    world.append(keeper)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
