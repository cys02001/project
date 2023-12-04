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
    ball_kick_sound = None
    shouting_sound=None
    boo_sound=None

    def __init__(self, x=400, y=20, velocity=1):
        self.isgoal = 0
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.ball_kick_sound = load_wav('ball_kick.wav')
        self.ball_kick_sound.set_volume(32)
        self.shouting_sound = load_wav('shouting.wav')
        self.shouting_sound.set_volume(32)
        self.boo_sound = load_wav('boo.wav')
        self.boo_sound.set_volume(48)

    def draw(self):
        self.image.draw(self.x, self.y, 40, 40)


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
        if group == 'ai_kicker:ball':
            self.ball_kick_sound.play()
            iscol = 2
            self.isgoal = 0
        if group == 'kicker:ball':
            self.ball_kick_sound.play()
            iscol = 2
            self.isgoal = 0
        if group == 'ai_keeper:ball':
            self.x = play_mode.ai_keeper.x
            self.y = play_mode.ai_keeper.y + 10
            self.isgoal = 0
            iscol = 1
        if group == 'keeper:ball':
            self.x = play_mode2.keeper.x
            self.y = play_mode2.keeper.y + 10
            self.isgoal = 0
            iscol = 1
        if group == 'ground:ball':
            self.isgoal = 1







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
                if not (self.x > 170 and self.x < 630 and self.y > 290 and self.y < 480):
                    self.isgoal=0
                iscol = 1
            elif play_mode.kicker.gauge_type == 1:
                self.x, self.y = play_mode.kicker.target_x, play_mode.kicker.target_y + 100
                if not (self.x > 170 and self.x < 630 and self.y > 290 and self.y < 480):
                    self.isgoal=0
                iscol = 1
            elif play_mode2.ai_kicker.gauge_type == 3:
                self.x, self.y = play_mode2.ai_kicker.target_x, play_mode2.ai_kicker.target_y
                if not (self.x > 170 and self.x < 630 and self.y > 290 and self.y < 480):
                    self.isgoal=0
                iscol = 1

        return self.x, self.y
