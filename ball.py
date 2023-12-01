from pico2d import *
import game_world
import play_mode
import play_mode2
import score

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

iscol = 1


class Ball:
    image = None
    def __init__(self, x=400, y=20, velocity=1):
        self.isgoal = 0
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y, 40, 40)
        draw_rectangle(*self.get_bb())

    def update(self):
        if iscol == 2:
            self.x, self.y = Ball.translate(self)
        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)

    # fill here
    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        global iscol


        if group == 'kicker:ball':
            iscol = 2
        if group == 'ai_kicker:ball':
            iscol = 2
        if group == 'ground:ball':
            if group == 'keeper:ball':
                self.x = play_mode2.keeper.x
                self.y = play_mode2.keeper.y + 10
            else:
                self.isgoal=1
                pass
            if group == 'ai_keeper:ball':
                self.x = play_mode.ai_keeper.x
                self.y = play_mode.ai_keeper.y + 10
            else:
                self.isgoal=1
                pass




    def translate(self):
        global iscol
        move_speed = 2
        if play_mode.kicker.gauge_type == 2:
            dx = play_mode.kicker.target_x - self.x
            dy = play_mode.kicker.target_y - self.y

        elif play_mode.kicker.gauge_type == 1:
            dx = play_mode.kicker.target_x - self.x
            dy = play_mode.kicker.target_y + 100 - self.y

        elif play_mode2.ai_kicker.gauge_type == 3:
            dx = play_mode2.ai_kicker.target_x - self.x
            dy = play_mode2.ai_kicker.target_y - self.y

        else:
            dx = 0
            dy = 0

        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist > move_speed:
            self.x += dx / dist * move_speed
            self.y += dy / dist * move_speed

        else:
            if play_mode.kicker.gauge_type == 2:
                self.x, self.y = play_mode.kicker.target_x, play_mode.kicker.target_y
                iscol = 1
            elif play_mode.kicker.gauge_type == 1:
                self.x, self.y = play_mode.kicker.target_x, play_mode.kicker.target_y + 100
                iscol = 1
            elif play_mode2.ai_kicker.gauge_type == 3:
                self.x, self.y = play_mode2.ai_kicker.target_x, play_mode2.ai_kicker.target_y
                iscol = 1

        return self.x, self.y
