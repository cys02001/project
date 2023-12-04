from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDL_QUIT, SDLK_SPACE

import game_framework
from pico2d import load_image, clear_canvas, update_canvas, get_events, load_font

import score
import title_mode


def init():
    global image
    global back_image
    global player_score_font
    global ai_score_font
    global player_font
    global ai_font
    global win_lose_font
    back_image = load_image('result_background.png')
    image = load_image('score.png')
    player_score_font = load_font('ENCR10B.TTF', 120)
    ai_score_font = load_font('ENCR10B.TTF', 120)
    player_font = load_font('ENCR10B.TTF', 36)
    ai_font = load_font('ENCR10B.TTF', 36)
    win_lose_font = load_font('ENCR10B.TTF', 150)

def finish():
    global image
    del image
    pass


def update():
    pass


def draw():
    clear_canvas()
    back_image.draw(400,300,800,600)
    image.draw(400, 300, 800, 600)
    if score.player_score> score.ai_score:
        win_lose_font.draw(250,150,'Win',(0,0,255))
    elif score.player_score<score.ai_score:
        win_lose_font.draw(200, 150, 'Lose', (255, 0, 0))
    player_score_font.draw(240, 290, str(score.player_score), (0, 0, 0))
    ai_score_font.draw(500, 290, str(score.ai_score), (0, 0, 0))
    player_font.draw(190, 380, 'Player', (0, 0, 0))
    ai_font.draw(530, 380, 'Ai', (0, 0, 0))
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
            score.turn=0
            score.player_score=0
            score.ai_score=0
            game_framework.change_mode(title_mode)
