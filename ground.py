from pico2d import load_image, draw_rectangle, load_music


class Ground:
    def __init__(self):
        self.image = load_image('ground.png')
        self.bgm = load_music('main_bgm.mp3')
        self.bgm.set_volume(128)
        self.bgm.repeat_play()

    def draw(self):
        self.image.draw(400, 300, 800, 600)
        draw_rectangle(*self.get_bb())


    def update(self):
        pass

    def get_bb(self):
        return 400 - 230, 300 - 10, 400 + 230, 300 + 180

    def handle_collision(self, group, other):
        if group == 'ground:ball':
            pass
