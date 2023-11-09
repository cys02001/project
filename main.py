from pico2d import open_canvas, delay, close_canvas
import logo_mode as start_mode
# import title_mode as start_mode
import game_framework
import play_mode

open_canvas()
# game_framework.run(start_mode)
game_framework.run(play_mode)
close_canvas()