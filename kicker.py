# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_d, delay,draw_rectangle
from ball import Ball
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION


# state event check
# ( state event type, event value )

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(kicker, e):
        kicker.frame = 0
        print('1')
        pass

    @staticmethod
    def exit(kicker, e):
        pass

    @staticmethod
    def do(kicker):

        pass

    @staticmethod
    def draw(kicker):
        kicker.image_kick.clip_draw(kicker.frame * 30, 0, 30, 80, kicker.x, kicker.y, 100, 200)


class Shooting:

    @staticmethod
    def enter(kicker, e):
        kicker.wait_time = get_time()
        kicker.ignore_input = True
        pass

    @staticmethod
    def exit(kicker, e):
        kicker.x = 300
        kicker.y = 0
        kicker.ignore_input = False
        kicker.frame = 0
        pass

    @staticmethod
    def do(kicker):
        if kicker.frame <= 5:
            kicker.frame = (kicker.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
            kicker.x += RUN_SPEED_PPS * game_framework.frame_time
            kicker.y += RUN_SPEED_PPS * game_framework.frame_time

        if get_time() - kicker.wait_time > 1:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            kicker.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(kicker):
        kicker.image_kick.clip_draw(int(kicker.frame) * 30, 0, 30, 80, kicker.x, kicker.y, 100, 200)

class StateMachine:
    def __init__(self, kicker):
        self.kicker = kicker
        self.cur_state = Idle
        self.transitions = {
            Idle: {d_down: Shooting},
            Shooting: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.kicker, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.kicker)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.kicker, e)
                self.cur_state = next_state
                self.cur_state.enter(self.kicker, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.kicker)

class Kicker:
    def __init__(self):
        self.x, self.y = 300, 0
        self.frame = 0
        self.image_kick = load_image('ai_kicker-removebg-preview.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def kick_ball(self):
        pass

    def get_bb(self):
        return self.x - 30, self.y - 60, self.x + 30, self.y - 20

    def handle_collision(self, group, other):
        if group == 'kicker:ball':
            print('2')





