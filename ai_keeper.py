# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_LSHIFT, SDLK_a, \
    SDLK_d, SDLK_w, delay, SDLK_q, SDLK_e,draw_rectangle

import play_mode
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


def type1(e):
    return e[0] == 'TYPE1'

def type2(e):
    return e[0] == 'TYPE2'

def type3(e):
    return e[0] == 'TYPE3'

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w


def q_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_q


def e_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e


# time_out = lambda e : e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(ai_keeper, e):
        ai_keeper.dir = 0
        ai_keeper.frame = 0
        ai_keeper.behavior = random.randint(1,3)
        pass

    @staticmethod
    def exit(ai_keeper, e):
        pass

    @staticmethod
    def do(ai_keeper):
        if play_mode.ball.y != 20:
            if ai_keeper.behavior == 1:
                ai_keeper.state_machine.handle_event(('TYPE1', 0))
            elif ai_keeper.behavior == 2:
                ai_keeper.state_machine.handle_event(('TYPE2', 0))
            elif ai_keeper.behavior == 3:
                ai_keeper.state_machine.handle_event(('TYPE3', 0))
        pass

    @staticmethod
    def draw(ai_keeper):
        ai_keeper.image.clip_draw(ai_keeper.frame * 20, 0, 20, 40, ai_keeper.x, ai_keeper.y, 80, 200)


class Jump_w:

    @staticmethod
    def enter(ai_keeper, e):
        ai_keeper.wait_time = get_time()
        ai_keeper.ignore_input = True
        ai_keeper.is_jumping = True
        pass

    @staticmethod
    def exit(ai_keeper, e):
        ai_keeper.y = 300
        ai_keeper.ignore_input = False
        ai_keeper.is_jumping = False
        pass

    @staticmethod
    def do(ai_keeper):
        ai_keeper.frame = 1
        ai_keeper.frame = (ai_keeper.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if ai_keeper.is_jumping:
            if ai_keeper.y < 400:  # 위로 점프 중
                ai_keeper.y += RUN_SPEED_PPS * game_framework.frame_time
            else:  # 점프 높이에 도달하면 아래로 내려오도록 변경
                ai_keeper.is_jumping = False

        if not ai_keeper.is_jumping and ai_keeper.y > 300:  # 점프가 끝났으면서 아직 땅에 닿지 않았을 때
            ai_keeper.y -= RUN_SPEED_PPS * game_framework.frame_time

        if get_time() - ai_keeper.wait_time > 3:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            ai_keeper.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(ai_keeper):
        ai_keeper.image.clip_draw(int(ai_keeper.frame) * 22, 0, 20, 60, ai_keeper.x, ai_keeper.y, 80, 200)


class Jump_q:

    @staticmethod
    def enter(ai_keeper, e):
        ai_keeper.frame = 0
        ai_keeper.wait_time = get_time()
        ai_keeper.ignore_input = True
        pass

    @staticmethod
    def exit(ai_keeper, e):
        ai_keeper.ignore_input = False
        ai_keeper.frame = 0
        pass

    @staticmethod
    def do(ai_keeper):
        if ai_keeper.frame <=2:
            ai_keeper.frame = ai_keeper.frame = (ai_keeper.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
            ai_keeper.x -= RUN_SPEED_PPS * game_framework.frame_time * 4

        if get_time() - ai_keeper.wait_time > 3:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            ai_keeper.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(ai_keeper):
        ai_keeper.image_jump.clip_draw(int(ai_keeper.frame) * 39, 0, 39, 60, ai_keeper.x, ai_keeper.y + 100, 100, 400)


class Jump_e:

    @staticmethod
    def enter(ai_keeper, e):
        ai_keeper.frame = 0
        ai_keeper.wait_time = get_time()
        ai_keeper.ignore_input = True
        pass

    @staticmethod
    def exit(ai_keeper, e):
        ai_keeper.ignore_input = False
        ai_keeper.frame = 0
        pass

    @staticmethod
    def do(ai_keeper):
        if ai_keeper.frame <= 2:
            ai_keeper.frame = ai_keeper.frame = (ai_keeper.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
            ai_keeper.x += RUN_SPEED_PPS * game_framework.frame_time * 4

        if get_time() - ai_keeper.wait_time > 3:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            ai_keeper.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(ai_keeper):
        ai_keeper.image_jump.clip_composite_draw(int(ai_keeper.frame) * 39, 0, 39, 60, 0, 'h', ai_keeper.x, ai_keeper.y + 100, 100, 400)


class StateMachine:
    def __init__(self, ai_keeper):
        self.ai_keeper = ai_keeper
        self.cur_state = Idle
        self.transitions = {
            Idle: {type1: Jump_w, type2: Jump_q, type3: Jump_e},
            Jump_q: {time_out: Idle}, Jump_e: {time_out: Idle}, Jump_w: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.ai_keeper, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.ai_keeper)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.ai_keeper, e)
                self.cur_state = next_state
                self.cur_state.enter(self.ai_keeper, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.ai_keeper)


class Ai_Keeper:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.dir = 0
        self.behavior = 0
        self.image = load_image('ai_keeper-removebg-preview.png')
        self.image_jump = load_image('keeper-jump.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def get_bb(self):
        return self.x - 10, self.y - 40, self.x + 20, self.y + 40

    def handle_collision(self, group, other):
        if group == 'ai_keeper:ball':
            pass
