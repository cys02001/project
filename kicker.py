# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_d, draw_rectangle, \
    SDLK_1, SDLK_2, SDLK_3, SDLK_5, delay
import game_framework
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
    def enter(kicker, e):
        kicker.gauge_point_updown = True
        kicker.frame = 0
        kicker.gauge_point_x = 400
        kicker.gauge_point_y = 100
        pass

    @staticmethod
    def exit(kicker, e):
        pass

    @staticmethod
    def do(kicker):
        play_mode.ball.x=400
        play_mode.ball.y=20
        if (kicker.gauge_point_x >= 200 and kicker.gauge_point_x <= 350) or (
                kicker.gauge_point_x >= 450 and kicker.gauge_point_x <= 600):
            kicker.gauge_type = 1
        elif kicker.gauge_point_x > 350 and kicker.gauge_point_x < 450:
            kicker.gauge_type = 2

        if kicker.gauge_point_x > 200 and kicker.gauge_point_updown == True:
            kicker.gauge_point_x -= 1
            if kicker.gauge_point_x == 200:
                kicker.gauge_point_updown = False
        if kicker.gauge_point_x < 600 and kicker.gauge_point_updown == False:
            kicker.gauge_point_x += 1
            if kicker.gauge_point_x == 600:
                kicker.gauge_point_updown = True


    @staticmethod
    def draw(kicker):
        kicker.image_kick.clip_draw(kicker.frame * 30, 0, 30, 80, kicker.x, kicker.y, 100, 200)
        kicker.image_target.clip_draw(kicker.frame * 30, 0, 500, 500, kicker.target_x, kicker.target_y, 40, 40)
        kicker.image_gauge_bar.draw(400, 100)
        kicker.image_gauge_point.draw(kicker.gauge_point_x, kicker.gauge_point_y, 5, 15)


class TargetMove:
    @staticmethod
    def enter(kicker, e):
        if num3_down(e) or num1_up(e):  # 오른쪽으로 Move
            kicker.dir = 1
            kicker.value = True
        elif num1_down(e) or num3_up(e):  # 왼쪽으로 Move
            kicker.dir = -1
            kicker.value = True
        if num5_down(e) or num2_up(e):  # 위로 Move
            kicker.updown = 1
            kicker.value = False
        elif num2_down(e) or num5_up(e):  # 아래로 Move
            kicker.updown = -1
            kicker.value = False
        kicker.frame = 0


    @staticmethod
    def exit(kicker, e):
        pass

    @staticmethod
    def do(kicker):
        play_mode.ball.x=400
        play_mode.ball.y = 20
        if kicker.value == True:
            kicker.target_x += kicker.dir * RUN_SPEED_PPS * game_framework.frame_time
        else:
            kicker.target_y += kicker.updown * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(kicker):
        kicker.image_kick.clip_draw(kicker.frame * 30, 0, 30, 80, kicker.x, kicker.y, 100, 200)
        kicker.image_target.clip_draw(kicker.frame * 30, 0, 500, 500, kicker.target_x, kicker.target_y, 40, 40)


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
        if play_mode.ball.isgoal == 1:
            score.player_score += 1
            play_mode.ball.shouting_sound.play()
            kicker.image_success_reaction.draw_now(40,40,200,200)
        elif play_mode.ball.isgoal == 0:
            play_mode.ball.boo_sound.play()
            kicker.image_fail_reaction.draw_now(40, 40, 200, 200)
        play_mode.ball.isgoal = 0
        delay(2)
        score.turn += 1
        game_framework.change_mode(play_mode2)
        play_mode.ball.x = 400
        play_mode.ball.y = 20
        kicker.gauge_type = 0
        pass

    @staticmethod
    def do(kicker):
        if kicker.frame <= 5:
            kicker.frame = (kicker.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
            kicker.x += RUN_SPEED_PPS * game_framework.frame_time
            kicker.y += RUN_SPEED_PPS * game_framework.frame_time

        if get_time() - kicker.wait_time > 3:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
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
            Idle: {d_down: Shooting, num1_down: TargetMove, num2_down: TargetMove, num1_up: TargetMove,
                   num2_up: TargetMove, num3_down: TargetMove, num5_down: TargetMove, num3_up: TargetMove,
                   num5_up: TargetMove},
            TargetMove: {num1_down: Idle, num2_down: Idle, num1_up: Idle, num2_up: Idle
                , num3_down: Idle, num5_down: Idle, num3_up: Idle, num5_up: Idle, d_down: Shooting},
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
        self.dir = 0
        self.updown = 0
        self.value = False
        self.target_x, self.target_y = 400, 300
        self.image_kick = load_image('player_kicker.png')
        self.image_target = load_image('target.png')
        self.image_gauge_bar = load_image('gauge_bar.png')
        self.image_gauge_point = load_image('gage_point.png')
        self.image_gauge_point.x = 400
        self.image_gauge_point.y = 100
        self.image_gauge_point_updown = True
        self.image_success_reaction = load_image('success_reaction.png')
        self.image_fail_reaction = load_image('fail_reaction.png')
        self.gauge_type = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()


    def get_bb(self):
        return self.x - 30, self.y - 60, self.x + 30, self.y - 20

    def handle_collision(self, group, other):
        if group == 'kicker:ball':
            pass
