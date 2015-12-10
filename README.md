# CSGOBombTimer
A simple python script to start a timer with an arduino when a signal is sent from CSGO
#Instructions
The code is basically split up into 3 sections
- CS config
- Python Listen Server
- Arduino Timer

##CS Config
This is the easiest to set up. Just drop the file `gamestate_integration_consolesample.cfg` into the csgo/cfg/ folder. If you can't run the listen server on port 3000, then you also need to change that in this file, otherwise just ignore it.

##Python Listen server
This was run on python 2.7, it can probably run on python 3.X with some slight modification. If you need to change the listen port, change that here and in CS. You will also need to set the Serial port in here, by default it is COM3, but yours may be different.

##Arduino timer
The arduino code I used is attached, but will likely require heavy modification from you. The concept as a whole is simple, wait until you recieve a message over serial, then start a 40 second (40,000 millisecond) timer, displaying it on a seven segment display. 
