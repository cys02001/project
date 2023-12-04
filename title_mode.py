from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDL_QUIT, SDLK_SPACE

import game_framework
from pico2d import load_image, clear_canvas, update_canvas, get_events, get_time, load_music, load_font

import game_world
import play_mode


def init():
    global image
    global font
    image = load_image('title.png')
    font = load_font('ENCR10B.TTF', 50)
def finish():
    global image
    del image
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(400, 300, 800, 600)
    font.draw(200,50,'Press to Start',(255,255,0))
    update_canvas()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)
