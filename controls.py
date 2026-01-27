import time
from machine import Pin

class Button:
    def __init__(self, pin_number, pull_up=True):
        mode = Pin.PULL_UP if pull_up else Pin.PULL_DOWN
        self.pin = Pin(pin_number, Pin.IN, mode)
        self.active_low = pull_up 
        self.prev_state = False    
        self.current_state = False 
        self.last_change_time = 0
        self.debounce_ms = 50

    def update(self):
        raw_reading = self.pin.value()
        is_pressed_now = not raw_reading if self.active_low else raw_reading

        now = time.ticks_ms()
        if is_pressed_now != self.current_state:
            if time.ticks_diff(now, self.last_change_time) > self.debounce_ms:
                self.prev_state = self.current_state 
                self.current_state = is_pressed_now  
                self.last_change_time = now
        else:
            self.prev_state = self.current_state

    def is_held(self):
        return self.current_state

    def was_pressed(self):
        return self.current_state and not self.prev_state
    