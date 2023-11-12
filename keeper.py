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


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w


def q_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_q


def e_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e


# time_out = lambda e : e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(keeper, e):
        keeper.dir = 0
        keeper.frame = 0
        pass

    @staticmethod
    def exit(keeper, e):
        pass

    @staticmethod
    def do(keeper):
        pass

    @staticmethod
    def draw(keeper):
        keeper.image.clip_draw(keeper.frame * 20, 0, 20, 40, keeper.x, keeper.y, 80, 200)
        keeper.image_kick.clip_draw(keeper.frame * 1, 0, 30, 80, 300, 0, 100, 200)  # 키커 임시로 띄우기
        keeper.image_ball.clip_draw(keeper.frame * 1, 0, 80, 80, 400, 20, 40, 40)  # 공 임시로 띄우기


class Move:

    @staticmethod
    def enter(keeper, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 Move
            keeper.dir = 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 Move
            keeper.dir = -1

    @staticmethod
    def exit(keeper, e):
        pass

    @staticmethod
    def do(keeper):
        keeper.frame = (keeper.frame + 1) % 1
        keeper.frame = (keeper.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1
        keeper.x += keeper.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(keeper):
        keeper.image.clip_draw(int(keeper.frame) * 33, 0, 20, 40, keeper.x, keeper.y, 80, 200)


class Jump_w:

    @staticmethod
    def enter(keeper, e):
        keeper.wait_time = get_time()
        keeper.ignore_input = True
        keeper.is_jumping = True
        pass

    @staticmethod
    def exit(keeper, e):
        keeper.y = 300
        keeper.ignore_input = False
        keeper.is_jumping = False
        pass

    @staticmethod
    def do(keeper):
        keeper.frame = 1
        keeper.frame = (keeper.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if keeper.is_jumping:
            if keeper.y < 400:  # 위로 점프 중
                keeper.y += RUN_SPEED_PPS * game_framework.frame_time
            else:  # 점프 높이에 도달하면 아래로 내려오도록 변경
                keeper.is_jumping = False

        if not keeper.is_jumping and keeper.y > 300:  # 점프가 끝났으면서 아직 땅에 닿지 않았을 때
            keeper.y -= RUN_SPEED_PPS * game_framework.frame_time

        if get_time() - keeper.wait_time > 1:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            keeper.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(keeper):
        keeper.image.clip_draw(int(keeper.frame) * 22, 0, 20, 60, keeper.x, keeper.y, 80, 200)


class Jump_q:

    @staticmethod
    def enter(keeper, e):
        keeper.frame = 0
        keeper.wait_time = get_time()
        keeper.ignore_input = True
        pass

    @staticmethod
    def exit(keeper, e):
        keeper.ignore_input = False
        keeper.frame = 0
        pass

    @staticmethod
    def do(keeper):
        if keeper.frame <=2:
            keeper.frame = keeper.frame = (keeper.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
            keeper.x -= RUN_SPEED_PPS * game_framework.frame_time * 2

        if get_time() - keeper.wait_time > 1:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            keeper.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(keeper):
        keeper.image_jump.clip_draw(int(keeper.frame) * 39, 0, 39, 60, keeper.x, keeper.y + 100, 100, 400)


class Jump_e:

    @staticmethod
    def enter(keeper, e):
        keeper.frame = 0
        keeper.wait_time = get_time()
        keeper.ignore_input = True
        pass

    @staticmethod
    def exit(keeper, e):
        keeper.ignore_input = False
        keeper.frame = 0
        pass

    @staticmethod
    def do(keeper):
        if keeper.frame <= 2:
            keeper.frame = keeper.frame = (keeper.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
            keeper.x += RUN_SPEED_PPS * game_framework.frame_time * 2

        if get_time() - keeper.wait_time > 1:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            keeper.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(keeper):
        keeper.image_jump.clip_composite_draw(int(keeper.frame) * 39, 0, 39, 60, 0, 'h', keeper.x, keeper.y + 100, 100, 400)


class StateMachine:
    def __init__(self, keeper):
        self.keeper = keeper
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Move, left_down: Move, left_up: Move, right_up: Move, w_down: Jump_w, q_down: Jump_q,
                   e_down: Jump_e},
            Move: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, w_down: Jump_w, q_down: Jump_q,
                   e_down: Jump_e},
            Jump_q: {time_out: Idle}, Jump_e: {time_out: Idle}, Jump_w: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.keeper, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.keeper)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.keeper, e)
                self.cur_state = next_state
                self.cur_state.enter(self.keeper, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.keeper)


class Keeper:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.dir = 0
        self.image = load_image('ai_keeper-removebg-preview.png')
        self.image_jump = load_image('keeper-jump.png')
        self.image_ball = load_image('ball21x21.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

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
