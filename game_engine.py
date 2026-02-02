import framebuf

import time 
class Sprite:
    def __init__(self, display, x, y, w, h, color, bitmap=None, vx=0, vy=0):
        self.display = display
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color 
        self.bitmap = bitmap 
        self.vx = vx
        self.vy = vy
        self.last_x = x
        self.last_y = y
        self.active = True
        self.drawn = False
        self.birth_time = 0

    def update(self):
        if not self.active: return
        self.last_x = self.x
        self.last_y = self.y
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        if not self.active:
            if self.last_x != -1:
                self.display.fill_rectangle(int(self.last_x), int(self.last_y), self.w, self.h, 0)
                self.last_x = -1
            return

        # Optimization: Only redraw if moved
        if  self.x != self.last_x or self.y != self.last_y:
            # 1. Erase old spot 
            self.display.fill_rectangle(int(self.last_x), int(self.last_y), self.w, self.h, 0)
            
            # 2. Draw New Sprite
            if self.bitmap:
                # Direct block write for images
                self.display.block(int(self.x), int(self.y), 
                                   int(self.x) + self.w - 1, 
                                   int(self.y) + self.h - 1, 
                                   self.bitmap)
            else:
                # Simple rectangle
                self.display.fill_rectangle(int(self.x), int(self.y), self.w, self.h, self.color)
        

    def check_collision(self, other):
        if not self.active or not other.active: return False
        return (self.x < other.x + other.w and
                self.x + self.w > other.x and
                self.y < other.y + other.h and
                self.y + self.h > other.y)


class Invader(Sprite):

    invader_last_move_time = 0   
    invader_speed = 10

    
    def __init__(self, display, x, y, w, h, color, bitmap=None, vx=0, vy=0):
        super().__init__(display, x, y, w, h, color, bitmap, vx, vy)
        
    
    def invader_update(self):
        if time.time_ns() > self.invader_last_move_time + 400000000:
            self.invader_last_move_time  = time.time_ns()
            self.x += self.invader_speed
            self.draw()
            self.update()

            if self.x > 290:
                self.invader_speed = -10
                
            if self.x < 0:
                self.invader_speed = 10

            if self.x > 290:
                self.y += 25
                self.update()
            if self.x < 0:
                self.y += 25
                self.update()

