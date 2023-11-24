from pico2d import *

import game_framework
import game_world
import title_mode
import random
from ground import Ground
from keeper import Keeper
from kicker import Kicker
from ball import Ball


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
            kicker.handle_event(event)


def init():
    global ground
    global keeper
    global kicker
    global ball
    global balls

    running = True

    ground = Ground()
    game_world.add_object(ground, 0)

    keeper = Keeper()
    game_world.add_object(keeper, 1)

    kicker = Kicker()
    game_world.add_object(kicker, 2)

    balls = [Ball(400, 20, 0) for _ in range(1)]
    game_world.add_objects(balls, 1)

    game_world.add_collision_pair('kicker:ball', kicker, None)
    game_world.add_collision_pair('keeper:ball', keeper, None)
    for ball in balls:
        game_world.add_collision_pair('kicker:ball', None, ball)
        game_world.add_collision_pair('keeper:ball', None, ball)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
