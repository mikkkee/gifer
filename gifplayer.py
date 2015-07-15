__author__ = 'Jianfeng'

from PyQt4 import QtGui


class GifPlayer(QtGui.QLabel):
    """Custom widget for QT Designer."""
    def __init__(self, parent=None):
        super(GifPlayer, self).__init__()
