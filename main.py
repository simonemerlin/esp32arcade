# main.py -- put your code here1
from machine import Pin, SPI
import ili9341, time
from game_engine import Sprite, Invader, Player, Laser
from controls import Button
from soundfx import SoundManager
from ui import Scoreboard
import urandom as rnd



### ======== DISPLAY AND SOUND
spi = SPI(1, baudrate=20000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
display = ili9341.Display(spi, cs=Pin(15), dc=Pin(2), rst=Pin(4), rotation = 90, height = 240, width = 320)
btn_fire = Button(26)
sfx = SoundManager(pin_number=25)
scoreboard = Scoreboard(display, 10, 10, color=0xFFFF)

### ============= CONFIGURAITON

invader_speed = 10
wait_before_new_laser = 0.42e9
num_invaders = 5
player_laser_speed = -15
invader_laser_speed = 5
invader_image = display.load_sprite("invader24x17.raw", 24, 17)

player_image = display.load_sprite("spaceship24x14.raw", 24, 14)

invader_speed = 0.3e9
score_to_win = 15


### ========= INITIALIZATION
def reset_game():
    display.clear()

    global game_state
    game_state = 'playing'
    
    
    global scoreboard
    scoreboard.reset()
    scoreboard.draw() 
    
    global player
    global player_image
    player = Player(display, x=230, y=200, w=24, h=14, bitmap= player_image, color=ili9341.color565(0, 0, 150))
    player.draw()
    
    global last_laser_time
    last_laser_time = 0
    
    global laserslist
    laserslist = []
    
    global invaders_list 
    invaders_list = []

    global invaders_lasers_list
    invaders_lasers_list = []
    
    global invader_speed
    invader_speed = 0.3e9

def reset_invaders():
    global invaders_list
    global invader_image
    for i in range(0, num_invaders): 
        invader = Invader(display, x=10 + i*40, y=20 , w=24, h=17,  bitmap = invader_image, id = i,  color=ili9341.color565(0, 255, 0))
        invaders_list.append(invader)

reset_game()

while True:
  
    btn_fire.update()
    if game_state == 'playing': 
        ### ============= PLAYER
        # update the player
        player.move()  
        abc = 0

        ### ============= PLAYER's LASERS
        # fire (Create a Laser Sprite) while button pressed. 
       
        if btn_fire.is_held():
            if time.time_ns() > last_laser_time + wait_before_new_laser:
                laserslist.append(Laser(display, x= round(player.x + player.w / 2 - 2.5), y=player.y-17, w=5, h=17, color=ili9341.color565(255, 0, 0), vy = player_laser_speed))
                sfx.play_shoot()
                last_laser_time = time.time_ns()     

        # update Lasers
        for l in laserslist:
            l.move()

        # check if any laser hit any invader. If an invader is hit, increase the score and delete the invader
        for l in laserslist:
            for i in invaders_list: 
                if i.check_collision(l):
                    l.delete() 
                    scoreboard.score +=1
                    scoreboard.draw()
                    i.delete() 
                
        # remove inactive lasers
        laserslist = [l for l in laserslist if l.active]

        if scoreboard.score >= score_to_win:
            game_state = 'you_won'

        ### ============== INVADERS
        #update invaders
        Invader.move_row(invader_speed)
        for invader in invaders_list: 
            invader.move(invader_speed)
            

        ### =============  INVADERS' LASERS    
        # each invader automatically firesa a Laser when its x poitions is same as the player x position
        for invader in invaders_list: 
            if invader.x >= player.x and invader.x <= player.x + player.w:
                if len(invader.lasers) == 0:  
                    invader.lasers.append(Laser(display, x= round(invader.x + invader.w / 2 - 2.5), y=invader.y+17, w=5, h=17, color=ili9341.color565(0, 255, 0), vy = invader_laser_speed))

        # update invaders Lasers and checl if they hit the player
        for invader in invaders_list: 
            if invader.check_collision(player):
                sfx.play_explosion()
                game_state = 'game_over'
                scoreboard.show_game_over()

            
            for l in invader.lasers: 
                if l.active:
                    l.move()
                    if l.check_collision(player):
                        sfx.play_explosion()
                        l.delete() 
                        invader.lasers = []
                       
                        game_state = 'game_over'
                        scoreboard.show_game_over()
                else:
                    invader.lasers = []
                


        invaders_list = [l for l in invaders_list if l.active]
        if len(invaders_list) == 0:
            reset_invaders()
            invader_speed -= 0.06e9

    elif game_state == 'you_won':
        if abc > 0:
            None
        else:
            scoreboard.show_you_won()   
            abc += 1   

        
        if btn_fire.was_pressed():
            reset_game()

    elif game_state == 'game_over':
        if btn_fire.was_pressed():
            reset_game()
   

    time.sleep(0.01)    