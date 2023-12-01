from pico2d import load_image, draw_rectangle


class Ground:
    def __init__(self):
        self.image = load_image('ground.png')
       # self.image_score = load_image('score.png')

    def draw(self):
        self.image.draw(400, 300, 800, 600)
        draw_rectangle(*self.get_bb())
       # self.image_score.draw(400,400,350,108)

    def update(self):
        pass

    def get_bb(self):
        return 400 - 230, 300 - 10, 400 + 230, 300 + 180

    def handle_collision(self, group, other):
        if group == 'ground:ball':
            pass
