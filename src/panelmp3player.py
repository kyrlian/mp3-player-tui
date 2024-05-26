""" MP3 panel """
#kyrlian, 2023

import os
from panel import Panel
from pygame import mixer
from paneldirectorybrowser import PanelDirectoryBrowser
import eventconverter

class PanelMp3Player(Panel):
    """ MP3 panel """

    def __init__(self, title="MP3 Player", initargs=None, status="normal"):
        Panel.__init__(self, title, initargs, status)
        self.panelcontrols=self.initpanelcontrols()
        self.panelcontrolstring = self.drawcontrols(self.panelcontrols," ")
        self.content = self.panelcontrolstring
        self.paused = True
        self.initialdirectory = initargs
        self.listoffset = 0
        self.playingtitle = ""
        mixer.init()

    def firstupdate(self):
        self.splitbrowser()

    def preferedsizes(self):
        self.sizes = [3, 10, len(self.content)+2]

    def updatecontent(self):
        """ update panel content """
        # If not paused and song is finished, go to next
        if not self.paused and not mixer.music.get_busy():
            self.forward()
            self.play()
        self.content = [self.panelcontrolstring, self.playingtitle]

    def stop(self):
        """ stop player """
        mixer.music.stop()

    def play(self):
        """ play song """
        if self.linkedpanel is not None and self.linkedpanel.currentfilenumber is not None:
            musicfile = self.linkedpanel.filelist[self.linkedpanel.currentfilenumber]
            musicdir = self.linkedpanel.currentdir
            musicfilepath = os.path.join(musicdir, musicfile)
            if os.path.isfile(musicfilepath):
                mixer.music.load( musicfilepath )
                mixer.music.play()
                self.playingtitle = musicfile.replace(".mp3","")

    def pause(self):
        """ pause song """
        if self.paused:
            mixer.music.unpause()
        if not self.paused:
            mixer.music.pause()
        self.paused = not self.paused

    def backward(self):
        """ go to previous song """
        if self.linkedpanel is not None and self.linkedpanel.currentfilenumber is not None:
            self.linkedpanel.currentfilenumber = max(self.linkedpanel.currentfilenumber-1 , 0)
            limit =  len(self.linkedpanel.filelist)
            while not self.linkedpanel.filelist[self.linkedpanel.currentfilenumber].endswith(".mp3") and limit > 0:#music file
                self.linkedpanel.currentfilenumber = max(self.linkedpanel.currentfilenumber-1 , 0)
                limit-=1
            self.play()

    def forward(self):
        """ go to next song """
        if self.linkedpanel is not None and self.linkedpanel.currentfilenumber is not None:
            self.linkedpanel.currentfilenumber = ( self.linkedpanel.currentfilenumber +1 ) %  len(self.linkedpanel.filelist) #loop
            limit = len(self.linkedpanel.filelist)
            while not self.linkedpanel.filelist[self.linkedpanel.currentfilenumber].endswith(".mp3") and limit > 0:#music file
                self.linkedpanel.currentfilenumber = ( self.linkedpanel.currentfilenumber +1 ) %  len(self.linkedpanel.filelist)
                limit-=1
            self.play()

    def splitbrowser(self):
        if  self.linkedpanel is None:
            if self.zone is not None :
                zPlayer, zBrowser = self.zone.split("h", .2,PanelDirectoryBrowser("MP3 Browser",[self.initialdirectory,".mp3"])) #split mp3 player zone horizontally, player will stay on top, add a file browser below
                zPlayer.panel.linkpanel(zBrowser.panel) # register the file browser with the mp3 player
                zBrowser.panel.registerfileclickaction(zPlayer.panel.play) # register the player play() method on browser click
        else:
            self.linkedpanel.remove()

    def initpanelcontrols(self):
        # "▣ > || << >>"
        playercontrols=[]#name,key,symbol,pos,command
        playercontrols.append(("Stop",None,"▣",[1],self.stop))
        playercontrols.append(("Play",None,">",[3],self.play))
        playercontrols.append(("Pause",eventconverter.KEY_SPACE,"||",[5,6],self.pause))
        playercontrols.append(("Bwd",eventconverter.KEY_RIGHT,"<<",[8,9],self.backward))
        playercontrols.append(("Fwd",eventconverter.KEY_LEFT,">>",[11,12],self.forward))
        playercontrols.append(("Browser",eventconverter.KEY_b,"B",[14],self.splitbrowser))
        return playercontrols
    
    def handleplayerclick(self, event,charx, chary):
        """ handle click on player controls """
        if self.zone is not None and chary == self.zone.y+1:
            for name,key,symbol,pos,command in self.panelcontrols:
                if charx - self.zone.x in pos:
                    print(f"clicked {name}")
                    command()
                    return

    def handlepanelclick(self, event, charx, chary):
        """ handle click on panel """
        self.handleplayerclick(event,charx, chary)
        self.handlecontrolclick(event, charx, chary)

    def handleplayerkeydown(self, event):
        """ handle player keys """
        for name,key,symbol,pos,command in self.panelcontrols:
            if event.key == key:
                print(f"Pressed {name}")
                command()
                return

    def handlepanelkeydown(self, event):
        self.handleplayerkeydown(event)
        self.handlecontrolkeydown(event)
