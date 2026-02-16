from machine import Pin, PWM
import time

class SoundManager:
    def __init__(self, pin_number):
        self.pin_number = pin_number
        self.buzzer = PWM(Pin(pin_number), freq=1000, duty=0)
        self.volume = 512 

    def play_shoot(self):
        self.buzzer = PWM(Pin(self.pin_number), freq=1000, duty=0)
        self.buzzer.duty(self.volume)
        for f in range(2000, 500, -200): 
            self.buzzer.freq(f)
            time.sleep_ms(5) 
        self.buzzer.duty(0)
        self.buzzer.deinit()
    def play_explosion(self):
        self.buzzer = PWM(Pin(self.pin_number), freq=1000, duty=0)
        
        import random
        self.buzzer.duty(self.volume)
        for _ in range(8):
            f = random.randint(50, 150)
            self.buzzer.freq(f)
            time.sleep_ms(15)
        self.buzzer.duty(0)
        self.buzzer.deinit()
        