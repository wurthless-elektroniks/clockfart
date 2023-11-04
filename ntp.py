#
# lamest copypaste of all time
# https://gist.github.com/aallan/581ecf4dc92cd53e3a415b7c33a1147c
#

import network
import socket
import time
import struct
import machine

import ntptime

import config
from config import WIFI_ENABLED,WIFI_NETWORK,WIFI_PASSWORD,WIFI_TIMEZONE_OFFSET

from machine import Pin

NTP_DELTA = 2208988800 + WIFI_TIMEZONE_OFFSET
host = "pool.ntp.org"

ssid = WIFI_NETWORK
password = WIFI_PASSWORD

tm_year = 0
tm_mon = 1 # range [1, 12]
tm_mday = 2 # range [1, 31]
tm_hour = 3 # range [0, 23]
tm_min = 4 # range [0, 59]
tm_sec = 5 # range [0, 61] in strftime() description
tm_wday = 6 # range 8[0, 6] Monday = 0
tm_yday = 7 # range [0, 366]
tm_isdst = 8 # 0, 1 or -1 

rtc=machine.RTC()
def set_time():
    # Get the external time reference
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()

    #Set our internal time
    val = struct.unpack("!I", msg[40:44])[0]
    tm = val - NTP_DELTA    
    t = time.gmtime(tm)
    rtc.datetime((t[0],t[1],t[2],t[6]+1,t[3],t[4],t[5],0))


def ntpSync(dst):
    if WIFI_ENABLED is True:
        try:
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            
            # grab connection first
            if True:
                wlan.connect(ssid, password)

                max_wait = 10
                while max_wait > 0:
                    if wlan.isconnected():
                        break
                    max_wait -= 1
                    print('waiting for connection...')
                    time.sleep(1)

                if wlan.status() != 3:
                    raise RuntimeError('network connection failed')
                else:
                    print('connected')
                    status = wlan.ifconfig()
                    print( 'ip = ' + status[0] )
            else:
                print(u"already locked on wifi, not bothering to connect.")
            
            ntptime.settime()
            t = time.localtime(time.time() + WIFI_TIMEZONE_OFFSET + (3600 if dst == 1 else 0))
            rtc.datetime((t[tm_year], t[tm_mon], t[tm_mday], t[tm_wday] + 1, t[tm_hour], t[tm_min], t[tm_sec], 0))
            print(time.localtime())
        finally:
            pass
    else:
        print(u"wifi not supported, exiting quietly.")