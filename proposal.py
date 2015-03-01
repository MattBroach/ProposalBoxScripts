from pyomxplayer import OMXPlayer
import RPi.GPIO as gp

from subprocess import call
import time

# Set pin layout to Pi Board
gp.setmode(gp.BOARD)

# List of output pins being used
OUTPUT = [10,12,16,18,22]

# Switch Input Pin
INPUT = 7

# Movie File
filename = 'Proposal.mp4'

# Pause time
pause = 65

# Initialize pins
for pin in OUTPUT:
    gp.setup(pin,gp.OUT)

gp.setup(INPUT,gp.IN)

omx = OMXPlayer(filename)


# Main loop
playing = False
prev_input = 0
start_time = time.time()
while True:
    # take a reading
    input = gp.input(INPUT)
    
    # Check for lid opening
    if(prev_input and (not input)):
        # Turn on screen
        call(['tvservice','-p'])
        time.sleep(4)

        # Play video
        omx.toggle_pause()

        # Set the playing flags
        playing = True
        start_time = time.time()
        

    # Check for lid closing
    if(input and (not prev_input)):
        # Turn off screen
        call(['tvservice','-o'])

        # Reset video
        omx.stop()
        time.sleep(.05)
        omx=OMXPlayer(filename)

        # Reset playing flags
        playing = False

        # Turn of LEDs
        for pin in OUTPUT:
            gp.output(pin,False)
    
    # If proper time has elpased since start
    # Turn on LEDs
    if playing:
        elapsed_time = time.time()-start_time
        if(elapsed_time > pause):
            playing = False
            for pin in OUTPUT:
                gp.output(pin,True)

    prev_input = input

    # Slight pause to debounce
    time.sleep(0.05)
