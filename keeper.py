# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT,SDLK_LSHIFT, SDLK_a,SDLK_d,SDLK_w,delay,SDLK_q,SDLK_e

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
        keeper.image.clip_draw(keeper.frame * 20, 0, 20, 40, keeper.x, keeper.y,80,200)



class Move:

    @staticmethod
    def enter(keeper, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 Move
            keeper.dir, keeper.face_dir= 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 Move
            keeper.dir, keeper.face_dir= -1, -1


    @staticmethod
    def exit(keeper, e):
        pass

    @staticmethod
    def do(keeper):
        keeper.frame = (keeper.frame + 1) % 1
        keeper.x += keeper.dir * 5
        pass

    @staticmethod
    def draw(keeper):
        keeper.image.clip_draw(keeper.frame * 33, 0, 20, 40, keeper.x, keeper.y,80,200)


class Jump_w:

    @staticmethod
    def enter(keeper, e):
        keeper.wait_time = get_time()
        keeper.ignore_input = True
        pass


    @staticmethod
    def exit(keeper, e):
        keeper.y=300
        keeper.ignore_input = False
        pass

    @staticmethod
    def do(keeper):
        keeper.frame = 1
        keeper.y +=1
        if get_time() - keeper.wait_time > 1:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            keeper.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(keeper):
        keeper.image.clip_draw(keeper.frame * 22, 0, 20, 60, keeper.x, keeper.y,80,200)


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
        pass

    @staticmethod
    def do(keeper):
        keeper.frame = (keeper.frame+1)%3
        keeper.x -= 1

        if get_time() - keeper.wait_time > 1:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            keeper.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(keeper):

        keeper.image_jump.clip_draw(keeper.frame * 39, 0, 39, 60, keeper.x, keeper.y+100,100,400)

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
        pass

    @staticmethod
    def do(keeper):
        keeper.frame = (keeper.frame + 1) % 3
        keeper.x += 1

        if get_time() - keeper.wait_time > 1:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            keeper.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(keeper):

        keeper.image_jump.clip_composite_draw(keeper.frame * 39, 0, 39, 60, 0, 'h', keeper.x, keeper.y + 100, 100, 400)


class Jump_a:

    @staticmethod
    def enter(keeper, e):
        keeper.frame = 2
        keeper.wait_time = get_time()
        keeper.ignore_input = True
        pass

    @staticmethod
    def exit(keeper, e):
        keeper.ignore_input = False
        pass

    @staticmethod
    def do(keeper):
        keeper.frame = keeper.frame
        keeper.x -= 1

        if get_time() - keeper.wait_time > 1:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            keeper.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(keeper):

        keeper.image_jump.clip_composite_draw(keeper.frame * 39, 0, 39, 60, 0, 'h', keeper.x, keeper.y + 100, 100, 400)


class Jump_d:

    @staticmethod
    def enter(keeper, e):
        keeper.frame = 2
        keeper.wait_time = get_time()
        keeper.ignore_input = True
        pass

    @staticmethod
    def exit(keeper, e):
        keeper.ignore_input = False
        pass

    @staticmethod
    def do(keeper):
        keeper.frame = keeper.frame
        keeper.x += 1

        if get_time() - keeper.wait_time > 1:  # 1초 경과 시 'TIME_OUT' 이벤트 생성
            keeper.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(keeper):

        keeper.image_jump.clip_composite_draw(keeper.frame * 39, 0, 39, 60, 0, 'h', keeper.x, keeper.y + 100, 100, 400)

class StateMachine:
    def __init__(self, keeper):
        self.keeper = keeper
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Move, left_down: Move, left_up: Move, right_up: Move, w_down: Jump_w, q_down: Jump_q, e_down: Jump_e,a_down: Jump_a,d_down: Jump_d},
            Move: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, w_down: Jump_w, q_down: Jump_q, e_down: Jump_e,a_down: Jump_a,d_down: Jump_d},
            Jump_q: {time_out: Idle}, Jump_e: {time_out: Idle}, Jump_w: {time_out: Idle}, Jump_a: {time_out: Idle},Jump_d: {time_out: Idle}
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
        self.face_dir = 1
        self.image = load_image('ai_keeper-removebg-preview.png')
        self.image_jump = load_image('ai_keeper-jump.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
