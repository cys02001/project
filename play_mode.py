from pico2d import *

import game_framework
import game_world
import title_mode
from ground import Ground
from keeper import Keeper


# Game object class here
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            keeper.handle_event(event)


def init():
    global running
    global ground
    global team
    global keeper

    running = True

    ground = Ground()
    game_world.add_object(ground, 0)

    keeper = Keeper()
    game_world.add_object(keeper, 1)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    keeper.wait_time = 1000000000000000.0
    pass

def resume():
    keeper.wait_time = get_time()
    pass

