import os
import sys
from playsound import playsound

# Not installable with poetry :(

if __name__ == "__main__":
    args = sys.argv[1:] 
    filepath = None if len(args) == 0 else args[0]
    playsound(filepath)