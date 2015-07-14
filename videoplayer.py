__author__ = 'Jianfeng'

from PyQt4.phonon import Phonon


class VideoPlayer(Phonon.VideoPlayer):
    """Custom widget for QT Designer."""
    def __init__(self):
        super(VideoPlayer, self).__init__()
