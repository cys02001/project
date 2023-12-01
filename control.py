from pico2d import *

import game_world
from ground import Ground
from keeper import Keeper
from kicker import Kicker
from ball import Ball
from ai_keeper import Ai_Keeper

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
            kicker.handle_event(event)


def create_world():
    global running
    global ground
    global keeper
    global kicker
    global ball

    running = True

    grass = Ground()
    game_world.add_object(ground, 0)

    keeper = Keeper()
    game_world.add_object(keeper, 1)

    kicker = Kicker()
    game_world.add_object(kicker, 2)

    ball = Ball()
    game_world.add_objects(ball, 3)

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
