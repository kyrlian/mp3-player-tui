
# Generated with websim.ai
# Prompt:
# an mp3 player in the terminal, using python textual and playsound
# https://websim.ai/c/pKYYRI86HUzJhQ4vH

# Basic textual layout, and playsound doesnt work :)

import os
from textual.app import App, ComposeResult
from textual.widgets import Button, DirectoryTree, Footer, Header, Static
from textual.containers import Container, Horizontal
from playsound import playsound

class MP3Player(App):
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 1fr 3fr;
    }
    
    #directory-tree {
        width: 100%;
        height: 100%;
    }
    
    #player-controls {
        width: 100%;
        height: 100%;
        layout: grid;
        grid-size: 1 4;
        content-align: center middle;
    }
    
    Button {
        width: 100%;
    }
    """

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.current_file = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield DirectoryTree(".", id="directory-tree")
        with Container(id="player-controls"):
            yield Static("No file selected", id="current-file")
            yield Button("Play", id="play-button", variant="success")
            yield Button("Stop", id="stop-button", variant="error")
            yield Button("Next", id="next-button", variant="primary")
        yield Footer()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        if event.path.suffix.lower() == ".mp3":
            self.current_file = event.path
            self.query_one("#current-file").update(f"Selected: {event.path.name}")
        else:
            self.current_file = None
            self.query_one("#current-file").update("Please select an MP3 file")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "play-button" and self.current_file:
            playsound(str(self.current_file), block=False)
            playsound()
        elif event.button.id == "stop-button":
            # Note: playsound doesn't have a built-in stop function
            # You might need to use a different library for more control
            pass
        elif event.button.id == "next-button":
            # Implement next track functionality
            pass

if __name__ == "__main__":
    app = MP3Player()
    app.run()
