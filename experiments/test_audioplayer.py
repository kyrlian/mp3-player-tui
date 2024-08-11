import os
import sys
from audioplayer import AudioPlayer


if __name__ == "__main__":
    args = sys.argv[1:] 
    filepath = None if len(args) == 0 else args[0]
    player = AudioPlayer(os.path.abspath(filepath))
    player.play(block=True)
