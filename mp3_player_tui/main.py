from turtle import st
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, DirectoryTree, Footer, Header, Static
from audioplayer import AudioPlayer
import os

class AudioCLI(App):
    """A Textual app to play audio files."""

    BINDINGS = [("q", "quit", "Quit"), ("p","playpause","Play/Pause")]
    debug = True
    player = None
    playing = False
    playing_file = ""
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Vertical(
            DirectoryTree(".", id="dir-tree"),
            Static("Please select an .mp3 file", id="status"),
            id="main",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Set up the app after mounting."""
        self.query_one(DirectoryTree).focus()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle file selection in the directory tree."""
        filepath = event.path
        filename, file_extension = os.path.splitext(filepath) 
        if file_extension == '.mp3':
            self.play_track(filepath)

    def play_track(self, filepath) -> None:
        """Play the selected track."""
        if self.player:
            self.player.stop()
        self.player = AudioPlayer(os.path.abspath(filepath))
        self.player.play()
        self.playing = True
        filename, file_extension = os.path.splitext(filepath)
        self.playing_file = filename
        self.query_one("#status").update(f"Now playing: {filename}")

    def action_playpause(self, play=None):
        if play is None:
            self.playing = not self.playing
        else:
            self.playing = play
        self.query_one("#status").update( self.playing_file + (" playing" if self.playing else " paused" ) )
        if self.player:
            if self.playing:
                self.player.resume()
            else:
                self.player.pause()

if __name__ == "__main__":
    app = AudioCLI()
    app.run()