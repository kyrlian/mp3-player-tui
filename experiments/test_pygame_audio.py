import os
import sys
from time import sleep
from pygame import mixer

# Not installable with poetry :(

if __name__ == "__main__":
    args = sys.argv[1:] 
    filepath = None if len(args) == 0 else args[0]

    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    while mixer.music.get_busy():
        sleep(1)
        