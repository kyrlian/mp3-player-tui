import os
import asyncio
import sys
from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree, Footer, Header, Static
from pygame import mixer

class AudioCLI(App):
    """A Textual app to play audio files."""

    BINDINGS = [("q", "quit", "Quit"), ("p","pause","Pause"), ("n","next","Next")]
    
    def __init__(self, *args, start_dir, **kwargs):
        mixer.init()
        self.paused = False
        self.playing_file = ""
        self.start_dir = start_dir
        self.status_msg = "Initializing..."
        super().__init__(*args, **kwargs)

        
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield DirectoryTree(path=self.start_dir, id="dir-tree")
        yield Static("Please select an .mp3 file", id="status")
        # yield Log("Please select an .mp3 file", id="status", auto_scroll=True)
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
            asyncio.create_task(self.play_track_and_next(filepath))

    def set_status(self, msg=None, save_status=True):
        if msg is None:
            msg = self.status_msg
        elif save_status:
            self.status_msg = msg
        # timestamp = datetime.now().strftime("%H:%M:%S")
        # self.query_one("#status", Log).write_line(f"{timestamp}: {msg}")
        self.query_one("#status", Static).update(msg)

    def find_next_file(self,filepath):
        if filepath is not None:
            filename = os.path.basename(filepath)
            filedir = os.path.dirname(filepath)
            #self.set_status(f"find_next_file: Looking for next after:{filename} filedir:{filedir}")
            getnext= False
            for f in os.listdir(filedir):
                if getnext:
                    fname, fextension = os.path.splitext(f) 
                    if fextension == '.mp3':
                        #self.set_status(f"find_next_file: Found next file: filedir:{filedir} f:{f}")            
                        self.query_one("#dir-tree", DirectoryTree).action_cursor_down()
                        return os.path.join(filedir, f)
                if f == filename:
                    getnext = True
            #self.set_status("find_next_file: No next file found")
        return None

    async def play_track_and_next(self, filepath):
        mixer.music.stop()
        self.paused = False
        while filepath is not None:
            filename, file_extension = os.path.splitext(filepath)
            self.set_status(f"Now playing: {os.path.basename(filename)}")
            self.playing_file = filename
            mixer.music.load(filepath)
            mixer.music.play()
            while mixer.music.get_busy() or self.paused:
                await asyncio.sleep(.1)
            self.set_status(f"Finished playing: {os.path.basename(filename)}")
            self.playing_file = None
            filepath = self.find_next_file(filepath)
    
    def action_next(self):
        n = self.find_next_file(self.playing_file)
        asyncio.create_task(self.play_track_and_next(n))

    def action_pause(self, paused=None):
        if self.playing_file is not None:
            if paused is None:
                self.paused = not self.paused
            else:
                self.paused = paused
            if self.paused:
                mixer.music.pause()
            else:
                mixer.music.unpause()
            self.set_status( os.path.basename(self.playing_file)  + (" paused" if self.paused else " playing" ) )

def main():
    args = sys.argv[1:]
    start_dir = "." if len(args) == 0 else args[0]    
    app = AudioCLI(start_dir=start_dir)
    app.run()    

if __name__ == "__main__":
    main()