# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_d, draw_rectangle, \
    SDLK_1, SDLK_2, SDLK_3, SDLK_5
import game_framework
import play_mode
import play_mode2
import score
import title_mode

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


def num1_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_1


def num1_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_1


def num2_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_2


def num2_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_2


def num3_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_3


def num3_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_3


def num5_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_5


def num5_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_5


def time_out(e):
    return e[0] == 'TIME_OUT'


# time_out = lambda e : e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(ai_kicker, e):
        ai_kicker.frame = 0
        ai_kicker.wait_time = get_time()
        print(score.turn)
        print('ai',score.ai_score)
        print('player',score.player_score)
        pass

    @staticmethod
    def exit(ai_kicker, e):
        pass

    @staticmethod
    def do(ai_kicker):
        play_mode.ball.x=400
        play_mode.ball.y=20

        if get_time() - ai_kicker.wait_time > 5:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            ai_kicker.state_machine.handle_event(('TIME_OUT', 0))


    @staticmethod
    def draw(ai_kicker):
        ai_kicker.image_kick.clip_draw(ai_kicker.frame * 30, 0, 30, 80, ai_kicker.x, ai_kicker.y, 100, 200)



class Shooting:

    @staticmethod
    def enter(ai_kicker, e):
        ai_kicker.wait_time = get_time()
        ai_kicker.ignore_input = True
        ai_kicker.target_x=random.randint(170,640)
        ai_kicker.target_y=random.randint(280,470)
        ai_kicker.gauge_type = 3
        pass

    @staticmethod
    def exit(ai_kicker, e):
        ai_kicker.x = 300
        ai_kicker.y = 0
        ai_kicker.ignore_input = False
        ai_kicker.frame = 0
        ai_kicker.gauge_type = 0
        ai_kicker.target_x = 0
        ai_kicker.target_y = 0
        play_mode2.ball.x = 400
        play_mode2.ball.y = 20
        if play_mode2.ball.isgoal == 1:
            score.ai_score += 1
        play_mode2.ball.isgoal = 0
        if score.turn >= 5:
            if score.player_score<score.ai_score:
                print('ai win')
                score.turn = 0
                score.player_score = 0
                score.ai_score = 0
                game_framework.change_mode(title_mode)
            elif score.player_score>score.ai_score:
                print('player win')
                score.turn = 0
                score.player_score = 0
                score.ai_score = 0
                game_framework.change_mode(title_mode)
            elif score.player_score == score.ai_score:
                game_framework.change_mode(play_mode)
        else:
            game_framework.change_mode(play_mode)
        pass

    @staticmethod
    def do(ai_kicker):
        if ai_kicker.frame <= 5:
            ai_kicker.frame = (ai_kicker.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
            ai_kicker.x += RUN_SPEED_PPS * game_framework.frame_time
            ai_kicker.y += RUN_SPEED_PPS * game_framework.frame_time

        if get_time() - ai_kicker.wait_time > 3:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            ai_kicker.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(ai_kicker):
        ai_kicker.image_kick.clip_draw(int(ai_kicker.frame) * 30, 0, 30, 80, ai_kicker.x, ai_kicker.y, 100, 200)


class StateMachine:
    def __init__(self, ai_kicker):
        self.ai_kicker = ai_kicker
        self.cur_state = Idle
        self.transitions = {
            Idle: {time_out: Shooting},
            Shooting: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.ai_kicker, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.ai_kicker)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.ai_kicker, e)
                self.cur_state = next_state
                self.cur_state.enter(self.ai_kicker, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.ai_kicker)


class Ai_Kicker:
    def __init__(self):
        self.x, self.y = 300, 0
        self.frame = 0
        self.value = False
        self.target_x, self.target_y = 0, 0
        self.image_kick = load_image('ai_kicker-removebg-preview.png')
        self.gauge_type = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 60, self.x + 30, self.y - 20

    def handle_collision(self, group, other):
        if group == 'ai_kicker:ball':
            pass
