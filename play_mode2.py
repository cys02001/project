from pico2d import *

import game_framework
import game_world
import title_mode
import play_mode
import random
from ground import Ground
from keeper import Keeper
from ai_kicker import Ai_Kicker
from ball import Ball


# Game object class here
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
        #     game_framework.change_mode(play_mode)
        else:
            keeper.handle_event(event)
            ai_kicker.handle_event(event)



def init():
    global ground
    global keeper
    global ai_kicker
    global ball
    global balls

    running = True

    ground = Ground()
    game_world.add_object(ground, 0)

    keeper = Keeper()
    game_world.add_object(keeper, 1)

    ai_kicker = Ai_Kicker()
    game_world.add_object(ai_kicker, 2)

    balls = [Ball(400, 20, 0) for _ in range(1)]
    game_world.add_objects(balls, 1)

    game_world.add_collision_pair('ai_kicker:ball', ai_kicker, None)
    game_world.add_collision_pair('keeper:ball', keeper, None)
    game_world.add_collision_pair('ground:ball', ground, None)
    for ball in balls:
        game_world.add_collision_pair('ai_kicker:ball', None, ball)
        game_world.add_collision_pair('keeper:ball', None, ball)
        game_world.add_collision_pair('ground:ball', None, ball)

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
