# main.py -- put your code here1
from machine import Pin, SPI
import ili9341, time
from game_engine import Sprite, Invader
from controls import Button
from soundfx import SoundManager
from ui import Scoreboard
spi = SPI(1, baudrate=20000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
display = ili9341.Display(spi, cs=Pin(15), dc=Pin(2), rst=Pin(4), rotation = 90, height = 240, width = 320)
player = Sprite(display, x=230, y=200, w=20, h=20, color=ili9341.color565(0, 0, 150))


sfx = SoundManager(pin_number=25)

btn_left = Button(14)
btn_right = Button(27)
btn_fire = Button(26)
btn_backward = Button(17)
btn_forward = Button(32)

scoreboard = Scoreboard(display, 10, 10, color=0xFFFF)


last_laser_time = 0
invader = Invader(display, x=150, y=20, w=20, h=20, color=ili9341.color565(0, 255, 0))
invader2 = Invader(display, x=125, y=20, w=20, h=20, color=ili9341.color565(0, 255, 0))

# makes the "invaders"
# player.draw()
# player.update()
# invader.draw()
# invader.update()
laserslist = []
invader_speed = 10

while True:
    btn_left.update()
    btn_right.update()
    btn_fire.update()
    btn_backward.update()
    btn_forward.update()

    player.update()
    
    if btn_left.is_held() and not btn_right.is_held():
        player.x -= 5
        player.x = max(player.x,0)
        player.draw()     
     
    if btn_right.is_held() and not btn_left.is_held():
        player.x += 5
        player.x = min(player.x,300)
        player.draw()

    if btn_forward.is_held():
        # player.y += 5 
        # player.draw() 
        None 
    if btn_backward.is_held():
       # player.y -= 5
       # player.draw()
       None
    if btn_fire.is_held():
        if time.time_ns() > last_laser_time + 420000000:
            laserslist.append(Sprite(display, x= round(player.x + player.w / 2 - 2.5), y=player.y-17, w=5, h=17, color=ili9341.color565(255, 0, 0), vy = -15))
            sfx.play_shoot()
            last_laser_time = time.time_ns()     
         
    for l in laserslist:
        l.update()
        l.draw()
        if l.y > 240-l.h:
            l.active = False

    laserslist = [l for l in laserslist if l.active]

    invader.invader_update()  
    invader2.invader_update()  


    time.sleep(0.02)
    
    