import framebuf
from controls import Button

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
        self.last_x = 0
        self.last_y = 0
        self.active = True
        self.drawn = False
        self.birth_time = 0

    def update(self):
        if not self.active: return
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        if not self.active:
            self.delete()
            # if self.last_x != -1:
            #     self.display.fill_rectangle(int(self.last_x), int(self.last_y), self.w, self.h, 0)
            #     self.last_x = -1
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
        self.last_x = self.x
        self.last_y = self.y


    def check_collision(self, other):
        if not self.active or not other.active: return False
        return (self.x < other.x + other.w and
                self.x + self.w > other.x and
                self.y < other.y + other.h and
                self.y + self.h > other.y)

    def delete(self):
        self.active = False
        self.display.fill_rectangle(int(self.last_x), int(self.last_y), self.w, self.h, 0)
        



class Player(Sprite):

    btn_left = Button(14)
    btn_right = Button(27)
   
    btn_backward = Button(17)
    btn_forward = Button(32)

    def __init__(self, display, x, y, w, h, color, bitmap=None, vx=0, vy=0):
        super().__init__(display, x, y, w, h, color, bitmap, vx, vy) 
    
    def move(self):
        self.btn_left.update()
        self.btn_right.update()
       
        self.btn_backward.update()
        self.btn_forward.update()
        #self.update()

        if self.btn_left.is_held() and not self.btn_right.is_held():
            self.x -= 5
            self.x = max(self.x,0)
            self.draw()     
        
        if self.btn_right.is_held() and not self.btn_left.is_held():
            self.x += 5
            self.x = min(self.x,300)
            self.draw()

        if self.btn_forward.is_held():
            # player.y += 5 
            # player.draw() 
            None 
        if self.btn_backward.is_held():
        # player.y -= 5
        # player.draw()
            None

class Invader(Sprite):

    
    def __init__(self, display, x, y, w, h, color, bitmap=None, vx=0, vy=0):
        super().__init__(display, x, y, w, h, color, bitmap, vx, vy) 
        self.invader_last_move_time = 0   
        self.invader_speed = 20
        self.lasers = []

    def move(self, speed = 0.3e9):
        if time.time_ns() > self.invader_last_move_time + speed :
            self.invader_last_move_time  = time.time_ns()
            self.x += self.invader_speed
         
            if self.x < 15:
                self.invader_speed += 40
                self.y += 40
                
            if self.x > 285:
                self.invader_speed -= 40
                self.y += 40

            if self.y > 240:
                self.y = 10
                       
        self.draw()
        #self.update()
    def delete(self): 
        super().delete()
        for l in self.lasers:
            l.delete()
       

class Laser(Sprite):
  
    def __init__(self, display, x, y, w, h, color, bitmap=None, vx=0, vy=0, target = []):
        super().__init__(display, x, y, w, h, color, bitmap, vx, vy) 
        self.last_move_time = 0   
        self.speed = 20
        self.target= target

    def move(self):
        if time.time_ns() > self.last_move_time + 30000000:
            self.last_move_time  = time.time_ns()
            self.y += self.vy
        if self.y < 0 or self.y > 240: 
            self.delete()
        else: 
            self.draw()
        # if not len(self.target) == 0: 
        #     if self.check_collision(self.target):
        #         sfx.play_explosion()
        #         self.active = False
            
               #self.update()
    
