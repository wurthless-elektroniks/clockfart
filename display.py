#
# all seven-segment display code goes here
#
import time
from machine import Pin, PWM
import rp2
from rp2 import PIO
from config import BRIGHTNESS_PWM_MAX

NUMBERS_TO_DIGITS = [
     0b00111111, # 0
     0b00000110, # 1 
     0b01011011, # 2
     0b01001111, # 3
     0b01100110, # 4
     0b01101101, # 5
     0b01111101, # 6
     0b00000111, # 7
     0b01111111, # 8
     0b01101111  # 9
]

g_active_digs_buffer = [
    # bits are right to left
    0b01110111,
    0b01101101,
    0b01101101,
    0b00000000
]

g_brightness = 8

g_brightness_pwm = PWM(Pin(10))

    
# lame copypaste https://wokwi.com/projects/300936948537623048
#
# segment drives on GPIOs 16,17,18,19,20,21,22
# column drives on GPIOS 12,13,14,15
@rp2.asm_pio(out_init=[PIO.OUT_LOW]*7, sideset_init=[PIO.OUT_LOW]*4)
def sevseg():
    wrap_target()
    label("0")
    pull(noblock)           .side(0)      # 0
    mov(x, osr)             .side(0)      # 1
    out(pins, 8)            .side(1)      # 2
    out(pins, 8)            .side(2)      # 3
    out(pins, 8)            .side(4)      # 4
    out(pins, 8)            .side(8)      # 5
    jmp("0")                .side(0)      # 6
    wrap()
      
sm = rp2.StateMachine(0, sevseg, freq=2000, out_base=Pin(16), sideset_base=Pin(12))


def displayStartup():
    sm.active(1)
    g_brightness = 8
    displaySetBrightness(8)

def displayKill():
    displaySetRawBits(0,0,0,0)
    displayRefresh()
    sm.active(0)
    
def displaySetBrightness(brightness):
    if brightness < 1:
        brightness = 1
    elif brightness > 8:
        brightness = 8

    g_brightness_pwm.freq(2000)
    g_brightness_pwm.duty_u16(int(65025 / (9 - brightness)))

def displaySetRawBrightness(brightness):
    g_brightness_pwm.freq(2000)
    g_brightness_pwm.duty_u16(int(brightness))

def displayRefresh():
    sm.put(
        g_active_digs_buffer[3] |
        g_active_digs_buffer[2] << 8 |
        g_active_digs_buffer[1] << 16 |
        g_active_digs_buffer[0] << 24
    )
    
def displaySetRawBits(segA, segB, segC, segD):
    g_active_digs_buffer[0] = segA
    g_active_digs_buffer[1] = segB
    g_active_digs_buffer[2] = segC
    g_active_digs_buffer[3] = segD
    displayRefresh()
    
#
# Set digits up.
# All segs must be numbers 0-9, if not then segs will be cleared
#
def displaySetDigs(segA, segB, segC, segD):
    
    if 0 <= segA and segA <= 9:
        g_active_digs_buffer[0] = NUMBERS_TO_DIGITS[segA]
    else:
        g_active_digs_buffer[0] = 0
    
    if 0 <= segB and segB <= 9:
        g_active_digs_buffer[1] = NUMBERS_TO_DIGITS[segB]
    else:
        g_active_digs_buffer[1] = 0
    
    if 0 <= segC and segC <= 9:
        g_active_digs_buffer[2] = NUMBERS_TO_DIGITS[segC]
    else:
        g_active_digs_buffer[2] = 0
    
    if 0 <= segD and segD <= 9:
        g_active_digs_buffer[3] = NUMBERS_TO_DIGITS[segD]
    else:
        g_active_digs_buffer[3] = 0
    
    displayRefresh()
