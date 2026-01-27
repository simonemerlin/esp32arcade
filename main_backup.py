# main.py -- put your code here1
from machine import Pin, SPI
import ili9341, time
from game_engine import Sprite
from controls import Button
from soundfx import SoundManager
from ui import Scoreboard

# --- Hardware Setup ---
# SPI1 on ESP32
spi = SPI(1, baudrate=20000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
display = ili9341.Display(spi, cs=Pin(15), dc=Pin(2), rst=Pin(4), rotation = 90, height = 240, width = 320)
sfx = SoundManager(pin_number=25)

# --- Inputs ---
btn_left = Button(14)
btn_right = Button(27)
btn_fire = Button(26)

# --- Global Objects ---
scoreboard = Scoreboard(display, 10, 10, color=0xFFFF)
player = None
lasers = []

# --- Reset Function ---
def reset_game():
    display.clear()
    scoreboard.reset()
    scoreboard.draw() 
    
    global player
    # Blue square player
    player = Sprite(display, x=230, y=160, w=20, h=20, color=ili9341.color565(255, 255, 0))
    
    global lasers
    lasers = []

# --- Initial Boot ---
reset_game()
game_state = "PLAYING" 

# --- Main Loop ---
while True:
    btn_left.update()
    btn_right.update()
    btn_fire.update()

    if game_state == "PLAYING":
        # 1. Player Movement
        
        player.update()
        
        if btn_left.is_held(): player.x -= 5
        if btn_right.is_held(): 
            player.x += 5
        
        # 2. Shooting
        if btn_fire.was_pressed():
        #if btn_fire.is_held():
        
            sfx.play_shoot()
            # Yellow laser
            new_laser = Sprite(display, x=player.x+8, y=player.y, w=4, h=10, 
                               color=ili9341.color565(255, 255, 0), vy=-8)
            lasers.append(new_laser)

        # 3. Update & Draw
        player.draw()
        
        for laser in lasers:
            laser.update()
            laser.draw()
            if laser.y < 0:
                laser.active = False
                scoreboard.score +=1
        
        lasers = [l for l in lasers if l.active]
        
        # 4. Score Logic (Example)
        if len(lasers) > 0: # Just to test score update
             # In real game, increment when laser hits enemy
             pass

        scoreboard.draw()        

        # 5. Game Over Trigger (Wall collision)
        if player.x <= 0 or player.x >= 300:
            sfx.play_explosion()
            game_state = "GAMEOVER"
            scoreboard.show_game_over() 

    elif game_state == "GAMEOVER":
        if btn_fire.was_pressed():
            game_state = "PLAYING"
            reset_game() 
            
    time.sleep(0.01)