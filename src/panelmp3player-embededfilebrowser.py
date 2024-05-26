""" MP3 panel """
#kyrlian, 2023

import os
from panel import Panel
from pygame import mixer
import pygame


class PanelMp3Player(Panel):
    """ MP3 panel """

    def __init__(self, title="MP3 Player", initargs=None, status="normal"):
        Panel.__init__(self, title, initargs, status)
        self.panelcontrols=self.initpanelcontrols()
        self.panelcontrolstring = self.drawpanelcontrols()# "▣ > || << >>"
        self.content = self.panelcontrolstring
        self.paused = True
        self.currentsongnumber = None
        self.musicdir = ""
        self.songlist = []
        self.loaddirectory(initargs)
        self.listoffset = 0
        self.playingtitle = ""
        mixer.init()

    def attachfilebrowser(self,directorybrowserpanelinstance):
        self.browser = directorybrowserpanelinstance

    def preferedsizes(self):
        self.sizes = [3, 10, len(self.content)+2]

    def loaddirectorycontent(self, directory,extension):
        """ load directory content """
        self.musicdir = directory
        self.songlist = [".."]
        for filename in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, filename)) or (os.path.isfile(os.path.join(directory, filename)) and filename.endswith(extension)):
                self.songlist.append(filename)
        if len(self.songlist) > 0:
            self.currentsongnumber = 0

    def loaddirectory(self, directory):
        """ load directory """
        if directory is not None and isinstance(directory, str) and os.path.isdir(directory):
            self.loaddirectorycontent(directory,".mp3")
        elif os.path.isdir("."):
            self.loaddirectorycontent(".",".mp3")
        elif os.path.isdir("C:/"):
            self.loaddirectorycontent("C:/",".mp3")
        else:
            print("No mp3 directory found")

    def listfilenames(self):
        """ list file names from songlist """
        displaylist = []
        for i in range(self.listoffset,len(self.songlist)):
            filename = self.songlist[i]
            if i == self.currentsongnumber:
                filename = "> "+filename
            displaylist.append(filename)
        return displaylist

    def updatecontent(self):
        """ update panel content """
        # If not paused and song is finished, go to next
        if not self.paused and not mixer.music.get_busy():
            self.forward()
            self.play()
        self.content = [self.panelcontrolstring, self.playingtitle]+self.listfilenames()

    def stop(self):
        """ stop player """
        mixer.music.stop()

    def play(self):
        """ play song """
        if self.currentsongnumber is not None:
            musicfile = self.songlist[self.currentsongnumber]
            musicfilepath = os.path.join(self.musicdir, musicfile)
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
        if self.currentsongnumber is not None:
            self.currentsongnumber = max(self.currentsongnumber-1 , 0)
            limit =  len(self.songlist)
            while not self.songlist[self.currentsongnumber].endswith(".mp3") and limit > 0:#music file
                self.currentsongnumber = max(self.currentsongnumber-1 , 0)
                limit-=1

    def forward(self):
        """ go to next song """
        if self.currentsongnumber is not None:
            self.currentsongnumber = ( self.currentsongnumber +1 ) %  len(self.songlist) #loop
            limit = len(self.songlist)
            while not self.songlist[self.currentsongnumber].endswith(".mp3") and limit > 0:#music file
                self.currentsongnumber = ( self.currentsongnumber +1 ) %  len(self.songlist)
                limit-=1

    def scrollup(self):
            self.listoffset = max(0, self.listoffset-1)

    def scrolldown(self):
            self.listoffset = min(len(self.songlist), self.listoffset+1)

    def initpanelcontrols(self):
        # "▣ > || << >>"
        playercontrols=[]#name,key,symbol,pos,command
        playercontrols.append(("Stop",None,"▣",[1],self.stop))
        playercontrols.append(("Play",None,">",[3],self.play))
        playercontrols.append(("Pause",pygame.K_SPACE,"||",[5,6],self.pause))
        playercontrols.append(("Bwd",pygame.K_RIGHT,"<<",[8,9],self.backward))
        playercontrols.append(("Fwd",pygame.K_LEFT,">>",[11,12],self.forward))
        playercontrols.append(("Up",pygame.K_UP,"^",[14],self.scrollup))
        playercontrols.append(("Down",pygame.K_DOWN,"v",[16],self.scrolldown))
        return playercontrols
    
    def drawpanelcontrols(self):
        # concat control symbols
        return " ".join(list(map(lambda tuple: tuple[2],self.panelcontrols)))

    def handleplayerclick(self, event,charx, chary):
        """ handle click on player controls """
        if self.zone is not None and chary == self.zone.y+1:
            for name,key,symbol,pos,command in self.panelcontrols:
                if charx - self.zone.x in pos:
                    print(f"clicked {name}")
                    command()
                    return

    def handlesongclick(self,event, charx, chary):
        """ handle click on song list """
        linecliked = chary - self.zone.y - 3 + self.listoffset  # skip controls and title, manage list offset
        if linecliked >= 0 and linecliked < len(self.songlist):
            if self.songlist[linecliked].endswith(".mp3"):#music file
                self.currentsongnumber = linecliked
                self.play()
            else:#directory
                newdir =  os.path.join(self.musicdir, self.songlist[linecliked])
                self.loaddirectory(newdir)

    def handlepanelclick(self, event, charx, chary):
        """ handle click on panel """
        self.handleplayerclick(event,charx, chary)
        self.handlesongclick(event,charx, chary)
        self.handlecontrolclick(event, charx, chary)

    def handleplayerkeydown(self, event, keymods):
        """ handle player keys """
        for name,key,symbol,pos,command in self.panelcontrols:
            if event.key == key:
                print(f"Pressed {name}")
                command()
                return

    def handlepanelkeydown(self, event, keymods):
        self.handleplayerkeydown(event, keymods)
        self.handlecontrolkeydown(event, keymods)
