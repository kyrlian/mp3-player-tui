from concurrent.futures import wait
from time import sleep
from turtle import st
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, DirectoryTree, Footer, Header, Static
from audioplayer import AudioPlayer
import os
import asyncio

class AudioCLI(App):
    """A Textual app to play audio files."""

    BINDINGS = [("q", "quit", "Quit"), ("p","playpause","Play/Pause")]
    debug = True
    player = None
    playing = False
    playing_file = ""
    status_msg="Initializing..."

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield DirectoryTree(".", id="dir-tree")
        yield Static("Please select an .mp3 file", id="status")
        yield Footer()

    def on_mount(self) -> None:
        """Set up the app after mounting."""
        self.query_one(DirectoryTree).focus()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle file selection in the directory tree."""
        filepath = event.path
        self.selected_dir = event.path
        filename, file_extension = os.path.splitext(filepath) 
        if file_extension == '.mp3':
            self.play_track_and_next(filepath)

    def set_status(self, msg=None, save_status=True):
        if msg is None:
            msg = self.status_msg
        elif save_status:
            self.status_msg = msg
        self.query_one("#status", Static).update(msg)

    def find_next_file(self,filepath):
        filename = os.path.basename(filepath)
        filedir = os.path.dirname(filepath)
        self.set_status(f"filename:{filename} filedir:{filedir}")
        getnext= False
        for f in os.listdir(filedir):
            if getnext:
                fname, fextension = os.path.splitext(f) 
                if fextension == '.mp3':
                    self.set_status(f"filedir:{filedir} f:{f}")
                    return os.path.join(filedir, f)
            if f == filename:
                getnext = True
        return None

    async def play_track(self, filepath):
        self.set_status(f"play_track {filepath} start")
        self.player = AudioPlayer(os.path.abspath(filepath))
        self.player.play(block=True)#TODO DEBUG: with block=True this always blocks (with or without async), even in a task - with block=False it starts playing and continue without waiting for the end
        self.set_status(f"play_track {filepath} end")
        
    def play_track_and_next(self, filepath) -> None:
        """Play the selected track and the next tracks in the directory"""
        if self.player:
            self.player.stop()
        while filepath is not None:
            filename, file_extension = os.path.splitext(filepath)
            self.playing_file = filename
            self.set_status(f"Now playing: {filename}")
            self.playing = True
            task = asyncio.create_task(self.play_track(filepath))
            # TODO DEBUG :
            # if play_track is NOT async - this never plays the next song (seems playtrack() becomes main thread and stops)
            # if play_track is async - this plays each song without waiting for the previous one to finish
            # => should be async
            self.set_status(f"Finished playing: {filename}")
            filepath = self.find_next_file(filepath)

    def action_playpause(self, play=None):
        if play is None:
            self.playing = not self.playing
        else:
            self.playing = play
        self.set_status( self.playing_file + (" playing" if self.playing else " paused" ) )
        if self.player:
            if self.playing:
                self.player.resume()
            else:
                self.player.pause()

def main():
    app = AudioCLI()
    app.run()    

if __name__ == "__main__":
    main()