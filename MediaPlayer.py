__author__ = 'saraiva'

''' This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import sys
from random import shuffle

from PyQt4 import QtCore, QtGui, uic

from PyQt4.phonon import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pickle


#Additional modules
import about, help

class MediaPlayer(QtGui.QMainWindow):
    '''
    This class represents the MediaPlayer main window and its auxiliary methods
    Controls: playlist, window buttons, etc.
    '''

    def __init__(self):
        # Initialize: calling the inherited __init__ function.
        super(MediaPlayer, self).__init__()

        # Load the defined UI.
        self.playlistSet = set()
        self.playlist = []
        self.current = -1
        self.total = 0
        self.ui = uic.loadUi('share/ui/Player.ui', self)
        self.initAttributes()
        self.videoState = 0

    def initAttributes(self):
        ''' Initialize class attributes and initial logic.
            1 - Set window sizes.
            2 - Link audio Output
            3 - Callbacks
        '''

        #: Maximize window
        self.showMaximized()

        #: Define timer to control certain user interactions
        self.Timer = QtCore.QTimer(self)
        self.Timer.setInterval(250)
        self.Timer.timeout.connect(self.on_Timer_timeout)
        self.Timer.start()

        #: Volume and slider control.
        self.volumeSlider.setAudioOutput(self.videoPlayer.audioOutput())
        self.seekSlider.setMediaObject(self.videoPlayer.mediaObject())

        #: Define a tick interval to control media playback time
        self.videoPlayer.mediaObject().setTickInterval(100)
        self.videoPlayer.mediaObject().tick.connect(self.tock)

        #: Menu bar actions.
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL('triggered()'), self.trigger_quit)
        QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL('triggered()'), self.trigger_about)
        QtCore.QObject.connect(self.actionHelp, QtCore.SIGNAL('triggered()'), self.trigger_help)
        QtCore.QObject.connect(self.actionSave_Playlist, QtCore.SIGNAL('triggered()'), self.trigger_save_playlist)
        QtCore.QObject.connect(self.actionOpen_Playlist, QtCore.SIGNAL('triggered()'), self.trigger_open_playlist)

        #: Events
        QtCore.QObject.connect(self.list, QtCore.SIGNAL('itemSelectionChanged()'), self.on_list_clicked)
        QtCore.QObject.connect(self.videoPlayer, QtCore.SIGNAL('finished()'), self.on_video_finished)
        #TODO parse dos tipos suportados para uma lista do tipo audio, video e imagem
        #use-> self.list.addItems(Phonon.BackendCapabilities.availableMimeTypes())

        #: Hotkeys

        #: Fullscreen
        self.shortcutFull = QtGui.QShortcut(self)
        self.shortcutFull.setKey(QtGui.QKeySequence('F12'))
        self.shortcutFull.setContext(QtCore.Qt.ApplicationShortcut)
        self.shortcutFull.activated.connect(self.on_btn_maximize_clicked)

        #: Exit
        self.shortcutQuit = QtGui.QShortcut(self)
        self.shortcutQuit.setKey(QtGui.QKeySequence("Alt+F4"))
        self.shortcutQuit.setContext(QtCore.Qt.ApplicationShortcut)
        self.shortcutQuit.activated.connect(self.trigger_quit)

    #: Open a previously saved playlist
    def trigger_open_playlist(self):
        # Create a file dialog to load the playlist.
        file_types = "Playlist (*.playlist);; All file (*.*)"
        filename, _ = QtGui.QFileDialog.getOpenFileNameAndFilter(self,
                                QtCore.QString("Load play list"), '', file_types)
        filename = unicode(filename.__str__())
        playlist_file = open(filename, 'rb')
        temp_playlist = pickle.load(playlist_file)
        if temp_playlist is None or not isinstance(temp_playlist, list):
            raise ValueError
        self.playlist = []
        self.playlistSet.clear()
        #: For each entry caught add to the current playlist
        for entry in temp_playlist:
            print entry
            self.playlistSet.add(entry)
        self.refresh_playlist()
        playlist_file.close()

    #: Save the current playlist
    def trigger_save_playlist(self):
        #: If playlist is empty do nothing
        if self.playlist is None or len(self.playlist) == 0:
            QMessageBox.about(self, "Warning", "There is nothing to save!")
        else:
            # Create a dialog showing the place to save the playlist.
            file_types = "Playlist (*.playlist);; All file (*.*)"
            filename, _ = QtGui.QFileDialog.getSaveFileNameAndFilter(self,
                            QtCore.QString("Save play list"), '', file_types)
            filename = unicode(filename.__str__())
            try:
                # save the playlist.
                playlist_file = open(filename, 'wb')
                pickle.dump(list(self.playlistSet), playlist_file)
                playlist_file.close()
                print "The play list is saved."
            except:
                QMessageBox.warning(self, "Sorry, the play list cannot be saved!")

    #: Triggers the program to quit
    def trigger_quit(self):
        if QMessageBox.warning(None, 'Confirm', "Are you sure you want to quit?",
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.No) == QMessageBox.Yes:
            QApplication.quit()

    #open about window
    def trigger_about(self):
        aboutDialog = about.About(parent=self)
        aboutDialog.show()

    #open help window
    def trigger_help(self):
        helpDialog = help.Help(parent=self)
        helpDialog.show()


###############################################################################################################
#
#       Timer methods and mouse
#
###############################################################################################################

    #: Response to timer event.
    @QtCore.pyqtSlot()
    def on_Timer_timeout(self):
        # Update the current mouse time and position.
        mousePos = QtGui.QCursor.pos()
        mouseY = self.mapFromGlobal(mousePos).y()
        mouseX = self.mapFromGlobal(mousePos).x()
        #print mouseX

        videoWidget = self.ui.videoPlayer.videoWidget()
        if videoWidget.isFullScreen():
            pass
        else:
            # TODO Adicionar suporte para teclas de controlo de video enquanto esta em fullscreen
            if mouseY > 650:
                pass

    #: Timer to count video time elapsed
    def tock(self, time):
        time = time/1000
        total = self.videoPlayer.totalTime() / 1000
        h1 = total/3600
        m1 = (total-3600*h1) / 60
        s1 = (total-3600*h1-m1*60)
        h = time/3600
        m = (time-3600*h) / 60
        s = (time-3600*h-m*60)
        self.lab_video_cur.setText('%02d:%02d:%02d'%(h,m,s))
        self.lab_video_tot.setText('/ %02d:%02d:%02d'%(h1,m1,s1))

    #: Catch double click event on main window here
    def mouseDoubleClickEvent(self, event):
        # Always, before process the event, we must send a copy of it to the
        # ancestor class.
        QtGui.QMainWindow.mouseDoubleClickEvent(self, event)
        # Go to full-screen mode or exit from it.
        self.on_btn_maximize_clicked()

###############################################################################################################
#
#       Initialize QT pre-determined Slots
#
###############################################################################################################
    @pyqtSlot()
    def on_btn_play_clicked(self):
        if self.current == -1:
            if len(self.playlist) > 0:
                self.current = 0
                self.list.setCurrentRow(self.current)
        self.play_current()

    @pyqtSlot()
    def on_btn_pause_clicked(self):
        self.videoPlayer.pause()
        self.videoState = 2

    @pyqtSlot()
    def on_btn_stop_clicked(self):
        self.videoPlayer.stop()
        self.videoState = 0

    @pyqtSlot()
    def on_btn_prev_clicked(self):
        if self.current <= 0:
            self.current = self.total-1
        else:
            self.current -= 1
        self.play_current()
        self.list.setCurrentRow(self.current)

    @pyqtSlot()
    def on_btn_next_clicked(self):
        if self.current >= self.total-1:
            self.current = 0
        else:
            self.current += 1
        self.play_current()
        self.list.setCurrentRow(self.current)

    @pyqtSlot()
    def on_btn_maximize_clicked(self):
        videoWidget = self.ui.videoPlayer.videoWidget()
        if videoWidget.isFullScreen():
            videoWidget.exitFullScreen()
            #self.showNormal()
            #self.list.show()
            #self.button_bar.show()
            #self.menubar.show()
            #self.ui.videoPlayer.resize(1150, 650)
        else:
            videoWidget.enterFullScreen()
            #self.showFullScreen()
            #self.list.hide()
            #self.button_bar.hide()
            #self.menubar.hide()
            #self.ui.videoPlayer.resize(1366, 768)

    @pyqtSlot()
    def on_btn_open_clicked(self):
        if self.videoState:
            self.videoPlayer.stop()
            self.self.videoState = 0
        # Create a dialog showing the place to save the playlist.
        file_types = "All files (*.*);;Images (*.jpg *.jpeg *bmp );;" \
                     "Audio (*.mp3 *.flac .m4a);;Videos (*.avi *.mp4 *.ogv *.avi *.tiff *mov)"
        dirpath = QtGui.QFileDialog.getOpenFileNames(self, "Select multimedia files only", '',file_types)
        if dirpath is not None:
            for file in dirpath:
                self.playlistSet.add(file)
            self.refresh_playlist()

    @pyqtSlot()
    def on_btn_equalizer_clicked(self):
        QMessageBox.about(self, "Warning", "There is nothing here!")

    @pyqtSlot()
    def on_btn_random_clicked(self):
        x = [[i] for i in range(self.total)]
        shuffle(x)
        temp = self.playlist
        self.list.clear()
        self.playlist = {}
        for i in range(self.total):
            item = temp[x[i][0]]
            self.playlist[i] = item
            self.list.addItem(item)
        self.current = 0
        self.videoPlayer.stop()
        self.videoState = 0

###############################################################################################################
#
#       Auxiliary methods
#
###############################################################################################################


    #callback when playlist item clicked
    def on_list_clicked(self, item):
        self.current = item.row()
        self.play_current()
        print 'selected item:\nIndex found at %s' \
              '\nWith data: %s' % (item.row(), item.data().toString())

    #Play the currently selected video
    def play_current(self):
        if self.videoState == 2:
            self.videoPlayer.play()
        else:
            self.label.setText('Now Playing: ' + self.playlist[self.current])
            for x in self.playlistSet:
                file = x.split('/')[-1]
                if file == self.playlist[self.current]:
                    self.videoPlayer.load(Phonon.MediaSource(x))
            self.videoPlayer.play()
        self.videoState = 1

    #Refresh playlist
    def refresh_playlist(self):
        self.list.clear()
        for x in self.playlistSet:
            file = x.split('/')[-1]
            self.playlist.append(file)
            self.list.addItem(file)
        self.total = len(self.playlist)

    #When video finishes play next
    def on_video_finished(self):
        if self.current >= self.total-1:
            return
        else:
            self.current += 1
        self.play_current()
        self.list.setCurrentRow(self.current)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Media Player')

    # Create a UI instance.
    MediaPlayer = MediaPlayer()

    # Show the UI.
    MediaPlayer.show()
    app.exec_()