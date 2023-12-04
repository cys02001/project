from pico2d import load_image, draw_rectangle, load_music, load_font

import score


class Ground:
    def __init__(self):
        self.image = load_image('ground.png')
        self.score_image = load_image('score.png')
        self.bgm = load_music('main_bgm.mp3')
        self.bgm.set_volume(128)
        self.bgm.repeat_play()
        self.player_font = load_font('ENCR10B.TTF', 16)
        self.ai_font = load_font('ENCR10B.TTF', 16)


    def draw(self):
        self.image.draw(400, 300, 800, 600)
        self.score_image.draw(400,550,80,60)
        self.player_font.draw(380, 550, str(score.player_score), (0, 0, 0))
        self.ai_font.draw(410, 550, str(score.ai_score), (0, 0, 0))
        self.player_font.draw(290, 550, 'Player', (0, 0, 255))
        self.ai_font.draw(450, 550, 'Ai', (255, 0, 0))



    def update(self):
        pass

    def get_bb(self):
        return 400 - 230, 300 - 10, 400 + 230, 300 + 180

    def handle_collision(self, group, other):
        if group == 'ground:ball':
            pass
