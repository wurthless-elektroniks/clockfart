import time
from machine import Pin, RTC
import rp2
from rp2 import PIO

import display
from display import displaySetDigs,displaySetRawBits,displayStartup

import ntp
from ntp import ntpSync

def getDst():
    f = open('dst','r')
    r = int(f.read())
    f.close()
    return r

def main():
    print(u"TMOUCITW starting up.")

    dst = getDst()
    displayStartup()
    
    # if DST button held, toggle DST on startup.
    dst_button = Pin(11, Pin.IN, Pin.PULL_UP)

    if dst_button.value() == 0:
        f = open('dst','w')
        dst = 0 if dst == 1 else 1
        f.write( '1' if dst == 1 else '0' )
        f.close()
        while True:
            # "DST ""
            displaySetRawBits(0b01011110, 0b01101101, 0b01111000, 0b00000000)
            time.sleep(0.5)
            # either "oFF " or "on  ""
            if dst == 1:
                displaySetRawBits(0b1011100, 0b01010100, 0b00000000, 0b00000000)
            else:
                displaySetRawBits(0b1011100, 0b01110001, 0b01110001, 0b00000000)
            time.sleep(0.5)


    # set display digits to 8888 while we try to sync to network time
    #displaySetDigs(8,8,8,8)

    
    # try locking to network time
    try:
        # 'SYNC'
        displaySetRawBits(0b01101101, 0b01101110, 0b00110111, 0b00111001)
        ntpSync(dst)
    except Exception as e:
        print(e)
        # 'ERR '
        displaySetRawBits(0b01111001, 0b01010000, 0b01010000, 0)
        return

    rtc=RTC()
    while True:
        t = time.localtime()
        displaySetDigs( int(t[3] / 10), int(t[3] % 10), int(t[4] / 10), int(t[4] % 10) )
        time.sleep(0.5)

main()
