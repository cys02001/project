# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_LSHIFT, SDLK_a, \
    SDLK_d, SDLK_w, delay, SDLK_q, SDLK_e
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

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(kicker, e):
        kicker.dir = 0
        kicker.frame = 0
        pass

    @staticmethod
    def exit(kicker, e):
        pass

    @staticmethod
    def do(kicker):
        pass

    @staticmethod
    def draw(kicker):
        kicker.image_kick.clip_draw(kicker.frame * 1, 0, 30, 80, 300, 0, 100, 200)  # 키커 임시로 띄우기

class StateMachine:
    def __init__(self, kicker):
        self.kicker = kicker
        self.cur_state = Idle
        self.transitions = {
            Idle: {},
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
        self.dir = 0
        self.image_kick = load_image('ai_kicker-removebg-preview.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
