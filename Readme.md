# Historical repository

[Continued development over here](https://github.com/wurthless-elektroniks/clock)

# About this code

[The Most Useless Clock in the World](https://github.com/wurthless-elektroniks/clock_v1) is being converted to run on cheaper hardware but the new software is still a work in progress. Until it is complete, the clocks I make will run this software.

# Hardware setup

* Your Pico W should have a reset button on it
* DST setting button goes to GPIO 11
* Segment drives on GPIOs 16,17,18,19,20,21,22
* Column drives on GPIOS 12,13,14,15
* Master output control transistor goes to GPIO 10 (optional as this code doesn't use brightness control at all)

# How to use

* Download the shittiest IDE of all time (Thonny)
* Connect Raspberry Pi Pico W to your computer
* Upload this sourcecode to the Pico using Thonny
* Change config.py with your Wi-Fi credentials and UTC offset
* Reboot the Pico
* If your clock displays the time, congratulations, it worked

# Toggling DST

Hold the DST button on power on/reset. Clock will toggle DST and display new setting ("DST ON" or "DST OFF").

# License

Public domain

Code has plenty of shitty copypastes in it that I don't know the licenses of and will not bother to find
