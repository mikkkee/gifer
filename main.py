__author__ = 'Jianfeng'

import sys

from PyQt4 import QtGui, QtCore, uic
from PyQt4.phonon import Phonon
from moviepy.editor import *

from videoplayer import VideoPlayer


class Info(object):
    """Info object used to hold user inputs"""

    def __init__(self):
        # Video name.
        self.video = None
        # Clip time.
        self.start = None
        self.end = None
        # Clip size.
        self.size = None
        self.scale = None
        # Mirror or not.
        self.mirrored = False
        # Default GIF writing options.
        self.fps = None
        self.fuzz = 1

    def update_video(self, name):
        """Update the video to process."""
        assert isinstance(name, str)
        self.video = name

    def update_time(self, start, end):
        """Update clip starting/ending time."""
        self.start, self.end = start, end

    def update_size(self, width, height, scale=None):
        """Update resize details of clip."""
        if scale is not None:
            self.scale = scale
        else:
            self.size = (width, height)

    def update_details(self, fps=None, fuzz=1, mirrored=False):
        """Add additional information."""
        self.fps = fps
        self.fuzz = fuzz
        self.mirrored = mirrored


class MagicBox(object):
    """A magic box which can convert videos into GIF pictures."""

    def __init__(self):
        self.clip = None
        self._original_clip = None
        self.info = Info()

    def make_clip(self):
        """Customize clip according to details in self.info"""
        # Init from video file.
        self.clip = VideoFileClip(self.info.video)
        # Create subclip.
        self.clip = self.clip.subclip(self.info.start, self.info.end)
        # Resize clip.
        if self.info.scale:
            self.clip = self.clip.resize(self.info.scale)
        else:
            self.clip = self.clip.resize(self.info.size)

    def save_gif(self, name):
        """Write VideoClip to a GIF file."""
        self.clip.write_gif(name, fps=self.info.fps, fuzz=self.info.fuzz)


class MagicBoxGui(QtGui.QMainWindow):
    """GUI for MagicBox."""

    def __init__(self):
        super(MagicBoxGui, self).__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.setWindowTitle('GIFer')

        # Define central widget.
        self.central_widget = MagicBoxCentralWidget()
        mirror_check_box = QtGui.QCheckBox('Mirror gif')

        # Attach central_widget to main window.
        self.setCentralWidget(self.central_widget)

        self.show()


class MagicBoxCentralWidget(QtGui.QWidget):
    """Central widget designed by QT Designer."""

    def __init__(self):
        super(MagicBoxCentralWidget, self).__init__()
        uic.loadUi('MagicBox.ui', self)

        media = Phonon.MediaSource('foam.mp4')
        print self.player
        self.player.play(media)


def main(argv):
    app = QtGui.QApplication(argv)
    mb = MagicBoxGui()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)






