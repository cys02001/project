from pico2d import *

import game_world
from ground import Ground
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


def create_world():
    global running
    global ground
    global team
    global keeper

    running = True

    grass = Ground()
    game_world.add_object(ground, 0)

    keeper = Keeper()
    game_world.add_object(keeper, 1)


open_canvas()
create_world()
# game loop
while running:
    handle_events()
    game_world.update()
    clear_canvas()
    game_world.render()
    update_canvas()
    delay(0.01)
# finalization code
close_canvas()
