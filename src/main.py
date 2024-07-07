# Generated with websim.ai
# Prompt:
# an mp3 player in the terminal, using python textual and audioplayer
# https://websim.ai/c/RdhSoPKFvkM0HbwLx

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, DirectoryTree, Footer, Header, Static
from textual.reactive import reactive
from audioplayer import AudioPlayer
import os

class AudioCLI(App):
    """A Textual app to play audio files."""

    CSS_PATH = "audio_cli.css"
    BINDINGS = [("q", "quit", "Quit")]
    debug = True
    player = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Vertical(
            DirectoryTree(".", id="dir-tree"),
            Vertical(
                Static("...", id="track-info"),
                Static("Please select an .mp3 file", id="status-info"),
                id="displays"
            ),
            Horizontal(
                Button("Play", id="play"),
                Button("Pause", id="pause"),
                Button("Stop", id="stop"),
                id="controls",
            ),
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
        filename, file_extension = os.path.splitext(filepath)
        self.query_one("#track-info").update(f"Now playing: {filename}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if self.debug: self.update_display(f"Pressed : {event.button.id}")
        if self.player:
            if event.button.id == "play":
                self.query_one("#status-info").update(f"Play")
                self.player.play()
            elif event.button.id == "pause":
                self.query_one("#status-info").update(f"Pause")
                self.player.pause()
            elif event.button.id == "stop":
                self.query_one("#status-info").update(f"Stop")
                self.player.stop()

if __name__ == "__main__":
    app = AudioCLI()
    app.run()