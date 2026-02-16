import ili9341
from xglcd_font import XglcdFont

class Scoreboard:
    def __init__(self, display, x, y, color=0xFFFF):
        self.display = display
        self.x = x
        self.y = y
        self.color = color
        self.score = 0
        self.old_score = -1 
        self.bg_color = 0x0000 
        self.arcadepix = XglcdFont('ArcadePix9x11.c', 9, 11)

    def increase(self, points):
        self.score += points

    def reset(self):
        self.score = 0
        self.old_score = -1

    def draw(self):
        if self.score != self.old_score:
            self.display.fill_rectangle(self.x, self.y, 60, 10, self.bg_color)
            score_str = "Score: {}".format(self.score)
            self.display.draw_text8x8(self.x, self.y, score_str, self.color, self.bg_color)
            self.old_score = self.score

    def show_game_over(self):
        self.display.fill_rectangle(60, 100, 200, 60, self.color)
        BLACK = 0x0000
        self.display.draw_text(124, 115, 'GAME OVER', self.arcadepix, BLACK, self.color)
        self.display.draw_text(110, 135, 'PRESS FIRE', self.arcadepix, BLACK, self.color)
    
    def show_you_won(self):
        self.display.fill_rectangle(60, 100, 200, 60, self.color)
        BLACK = 0x0000
        self.display.draw_text(124, 115, 'YOU WON!', self.arcadepix, BLACK, self.color)
        self.display.draw_text(110, 135, 'PRESS FIRE', self.arcadepix, BLACK, self.color)