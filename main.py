__author__ = 'Jianfeng'

import sys
import os

from PyQt4 import QtGui, QtCore
from moviepy.editor import *
import moviepy.video.fx.all as afx
from central_widget_ui import Ui_Form


class Info(object):
    """Info object used to hold user inputs"""

    def __init__(self):
        # Video name.
        self.video = None
        # Clip time.
        self.original_duration = None
        self.start = None
        self.end = None
        # Clip size.
        self.original_size = None
        self.width = None
        self.height = None
        self.scale = None
        # Mirror or not.
        self.mirrored = False
        # Default GIF writing options.
        self.original_fps = None
        self.fps = None
        self.fuzz = 1

    @property
    def size(self):
        return [self.width, self.height]

    def is_valid(self):
        """Validate whether existing parameters are enough to make a GIF picture."""
        return all([x is not None for x in [self.video, self.start, self.end]])

    def update_video(self, name):
        """Update the video to process."""
        assert isinstance(name, str)
        self.video = name

    def update_start(self, start=None):
        """Update clip starting time."""
        if start is not None:
            self.start = float(start)

    def update_end(self, end=None):
        """Update clip ending time."""
        if end is not None:
            self.end = float(end)

    def update_width(self, width=None):
        """Update clip resize width."""
        if width is not None:
            self.width = float(width)

    def update_height(self, height=None):
        """Update clip resize height."""
        if height is not None:
            self.height = float(height)

    def update_scale(self, scale=None):
        """Update clip resize scale."""
        if scale is not None:
            self.scale = float(scale)
        else:
            self.scale = None

    def update_fps(self, fps=None):
        if fps:
            self.fps = float(fps)
        else:
            self.fps = None

    def update_fuzz(self, fuzz=None):
        if fuzz:
            self.fuzz = float(fuzz)
        else:
            self.fuzz = None

    def update_mirror(self, mirrored=None):
        if mirrored is not None:
            self.mirrored = mirrored


class ConsoleCapture(QtCore.QObject):
    """Capture MoviePy console output to show on status bar."""

    text_written = QtCore.pyqtSignal(str)
    text_content = None

    def write(self, text):
        self.text_content = text
        self.text_written.emit(self.text_content)

    def flush(self):
        self.text_written.emit(self.text_content)


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
        # Create sub-clip.
        self.clip = self.clip.subclip(self.info.start, self.info.end)
        # Resize clip.
        if self.info.scale:
            self.clip = self.clip.resize(self.info.scale)
        else:
            self.clip = self.clip.resize(self.info.size)

    def save_gif(self, name):
        """Write VideoClip to a GIF file."""
        if self.info.mirrored:
            self.clip = afx.time_symmetrize(self.clip)
        self.clip.write_gif(name, fps=self.info.fps, fuzz=self.info.fuzz)


class MagicBoxGui(QtGui.QMainWindow):
    """GUI for MagicBox."""

    def __init__(self):
        super(MagicBoxGui, self).__init__()
        self.magic_box = MagicBox()
        self.central_widget = MagicBoxCentralWidget()
        self.loaded_gif = None  # GIF to be loaded in the player.
        self.last_video_dir = QtCore.QString()  # Last directory where user opened a video, default is current dir.
        self.last_gif_dir = QtCore.QString()  # Last directory where user saved a gif, default is current dir.
        sys.stdout = ConsoleCapture(text_written=self.update_status_bar_gif_progress)
        self.initUI()

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.setWindowTitle('GIFer')

        # Menu bar - open video
        open_file = QtGui.QAction('Open Video', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Open New Video')
        open_file.triggered.connect(self.show_open_video_dialog)
        # Menu bar - open GIF
        open_gif = QtGui.QAction('Open GIF', self)
        open_gif.setShortcut('Ctrl+G')
        open_gif.setStatusTip('Open New GIF Picture')
        open_gif.triggered.connect(self.show_open_gif_dialog)
        # Menu bar - exit program
        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QtGui.qApp.quit)

        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        file_menu.addAction(open_file)
        file_menu.addAction(open_gif)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        ########### Setup central widget ##########

        # Validators.
        double_validator = QtGui.QDoubleValidator(self)
        double_validator.setBottom(0)
        percent_validator = QtGui.QDoubleValidator(self)
        percent_validator.setRange(0, 100, 2)

        self.central_widget.start_input.setValidator(double_validator)
        self.central_widget.end_input.setValidator(double_validator)
        self.central_widget.width_input.setValidator(double_validator)
        self.central_widget.height_input.setValidator(double_validator)
        self.central_widget.fps_input.setValidator(double_validator)
        self.central_widget.scale_input.setValidator(double_validator)
        self.central_widget.fuzz_input.setValidator(percent_validator)

        # Signals and slots.
        # LineEdits
        self.central_widget.start_input.textChanged.connect(
            self.handle_start_change)
        self.central_widget.end_input.textChanged.connect(
            self.handle_end_change)
        self.central_widget.width_input.textChanged.connect(
            self.handle_width_change)
        self.central_widget.height_input.textChanged.connect(
            self.handle_height_change)
        self.central_widget.scale_input.textChanged.connect(
            self.handle_scale_value_change)
        self.central_widget.fps_input.textChanged.connect(
            self.handle_fps_change)
        self.central_widget.fuzz_input.textChanged.connect(
            self.handle_fuzz_change)
        # Checkboxes
        self.central_widget.scale_check.stateChanged.connect(
            self.handle_scale_state_change)
        self.central_widget.mirror_check.stateChanged.connect(
            self.handle_mirrored_change)
        # PushButtons
        self.central_widget.generate_btn.clicked.connect(
            self.generate_gif)
        self.central_widget.reset_btn.clicked.connect(self.reset_parameters)
        # GIF Player
        self.central_widget.play_btn.clicked.connect(self.play_loaded_gif)
        self.central_widget.pause_btn.clicked.connect(self.pause_loaded_gif)
        self.central_widget.stop_btn.clicked.connect(self.stop_loaded_gif)
        self.central_widget.next_frame_btn.clicked.connect(self.next_frame_loaded_gif)

        # Set initial state for widgets in central_widget.
        self.central_widget.scale_input.setDisabled(True)
        self.central_widget.gif_player.setAlignment(QtCore.Qt.AlignCenter)

        # Attach central_widget to main window.
        self.setCentralWidget(self.central_widget)
        self.move(100, 100)

        self.show()

    def show_open_video_dialog(self):
        """Open video file to be processed."""
        # Default open directory is current directory.
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open Video File', self.last_video_dir)
        self.last_video_dir = QtCore.QString(os.path.dirname(str(fname)))

        if not fname:
            # In case user closed open file dialog.
            return

        # Update movie name in statusBar.
        msg = 'Selected: {name}'.format(name=fname)
        self.statusBar().showMessage(msg)

        # Update video info - resolution, duration, fps.
        self.magic_box.info.update_video(str(fname))
        self.magic_box.clip = VideoFileClip(str(fname))
        duration = self.magic_box.clip.duration
        self.magic_box.info.original_duration = duration
        w, h = self.magic_box.clip.size
        self.magic_box.info.original_size = (w, h)
        fps = self.magic_box.clip.fps
        self.magic_box.original_fps = fps

        # Update video info in main window.
        self.central_widget.start_input.setText('0')
        self.central_widget.end_input.setText(str(duration))
        self.central_widget.width_input.setText(str(w))
        self.central_widget.height_input.setText(str(h))
        self.central_widget.fps_input.setText(str(fps))

    def show_open_gif_dialog(self):
        """Open GIF file and load it to GIF player."""
        gif_name = QtGui.QFileDialog.getOpenFileName(
                self, 'Open GIF File', self.last_gif_dir,
                "GIF (*.gif)")
        if gif_name:
            self.last_gif_dir = QtCore.QString(os.path.dirname(str(gif_name)))
            self.load_gif(gif_name)

    def update_status_bar_gif_progress(self, text):
        self.statusBar().showMessage(text)

    def reset_parameters(self):
        if self.magic_box.info.video:
            self.central_widget.start_input.setText('0')
            self.central_widget.end_input.setText(str(self.magic_box.info.original_duration))
            self.central_widget.width_input.setText(str(self.magic_box.info.original_size[0]))
            self.central_widget.height_input.setText(str(self.magic_box.info.original_size[1]))
            self.central_widget.fps_input.setText(str(self.magic_box.info.original_fps))
        else:
            self.central_widget.start_input.setText('')
            self.central_widget.end_input.setText('')
            self.central_widget.width_input.setText('')
            self.central_widget.height_input.setText('')
            self.central_widget.fps_input.setText('')
        self.central_widget.scale_check.setCheckState(0)
        self.central_widget.mirror_check.setCheckState(0)

    def resizeEvent(self, event):
        """Customize the resizeEvent() inherited from QWidget."""
        super(MagicBoxGui, self).resizeEvent(event)
        if self.loaded_gif:
            size = self.central_widget.gif_player.size()
            self.resize_loaded_gif(size)

    def generate_gif(self):
        if self.magic_box.info.is_valid():
            if self.loaded_gif:
                # Close opened gif.
                self.loaded_gif.setFileName(QtCore.QString())
            self.magic_box.make_clip()
            gif_name = QtGui.QFileDialog.getSaveFileName(
                self, 'Save GIF File', self.last_gif_dir,
                "GIF (*.gif)")

            if gif_name:
                self.last_gif_dir = QtCore.QString(os.path.dirname(str(gif_name)))
                self.magic_box.save_gif(str(gif_name))

            # Open GIF file after saved.
            self.load_gif(str(gif_name))

    def load_gif(self, gif_name):
        self.loaded_gif = QtGui.QMovie()
        self.loaded_gif.setFileName(gif_name)
        player_size = self.central_widget.gif_player.size()
        self.central_widget.gif_player.setMovie(self.loaded_gif)
        self.loaded_gif.frameChanged.connect(self.update_status_bar_frame_number)
        self.loaded_gif.start()
        self.resize_loaded_gif(player_size)

    def resize_loaded_gif(self, size):
        """Resize movie to size while keeping its aspect ratio."""
        movie = self.loaded_gif
        snapshot = movie.currentImage()
        current_size = snapshot.size()
        current_width = float(current_size.width())
        current_height = float(current_size.height())
        screen_width = float(size.width())
        screen_height = float(size.height())
        if screen_height / screen_width > current_height / current_width:
            # Need to scale by screen width
            new_width = int(screen_width)
            new_height = int(current_height * new_width / current_width)
        else:
            # Need to scale by screen height.
            new_height = int(screen_height)
            new_width = int(current_width * new_height / current_height)
        movie.setScaledSize(QtCore.QSize(new_width, new_height))

    def update_status_bar_frame_number(self, frame):
        message = 'Frame: {frame}/{total_frame}'.format(frame=frame, total_frame=self.loaded_gif.frameCount())
        self.statusBar().showMessage(message)

    def play_loaded_gif(self):
        if self.loaded_gif:
            self.loaded_gif.start()

    def pause_loaded_gif(self):
        if self.loaded_gif:
            self.loaded_gif.setPaused(True)

    def stop_loaded_gif(self):
        if self.loaded_gif:
            self.loaded_gif.stop()

    def next_frame_loaded_gif(self):
        if self.loaded_gif:
            self.loaded_gif.jumpToNextFrame()

    def jump_to_frame_loaded_gif(self, number):
        """Jump to a frame.
        Cannot jump back."""
        if self.loaded_gif:
            self.loaded_gif.jumpToFrame(min(number, self.loaded_gif.frameCount() - 1))

    def handle_start_change(self, start):
        if start:
            self.magic_box.info.update_start(start)

    def handle_end_change(self, end):
        if end:
            self.magic_box.info.update_end(end)

    def handle_width_change(self, width):
        if width:
            self.magic_box.info.update_width(width)
            if not self.central_widget.height_input.text() and self.magic_box.info.video:
                # Update height if height input is empty and there is video opened.
                height = float(width) / self.magic_box.info.original_size[0] * self.magic_box.info.original_size[1]
                self.central_widget.height_input.setText(str(height))

    def handle_height_change(self, height):
        if height:
            self.magic_box.info.update_height(height)
            if not self.central_widget.width_input.text() and self.magic_box.info.video:
                # Update width if width input is empty and there is video opened.
                width = float(height) / self.magic_box.info.original_size[1] * self.magic_box.info.original_size[0]
                self.central_widget.width_input.setText(str(width))

    def handle_scale_state_change(self, scale_state):
        scaled = bool(scale_state)

        self.central_widget.width_input.setDisabled(scaled)
        self.central_widget.height_input.setDisabled(scaled)
        self.central_widget.scale_input.setDisabled(not scaled)

        if scaled and self.magic_box.info.video:
            width, height = self.magic_box.info.original_size
            self.central_widget.width_input.setText(str(width))
            self.central_widget.height_input.setText(str(height))
        else:
            # Set scale in Info() to None.
            self.magic_box.info.update_scale(None)

    def handle_scale_value_change(self, scale_ratio):
        ratio = float(scale_ratio)

        self.magic_box.info.update_scale(ratio)

        width, height = ratio * self.magic_box.info.original_size[0], ratio * self.magic_box.info.original_size[1]
        self.central_widget.width_input.setText(str(width))
        self.central_widget.height_input.setText(str(height))

    def handle_fps_change(self, fps):
        if fps:
            self.magic_box.info.update_fps(fps)

    def handle_fuzz_change(self, fuzz):
        if fuzz:
            self.magic_box.info.update_end(fuzz)

    def handle_mirrored_change(self, mirrored):
        if mirrored:
            self.magic_box.info.update_mirror(True)
        else:
            self.magic_box.info.update_mirror(False)


class MagicBoxCentralWidget(QtGui.QWidget, Ui_Form):
    """Central widget designed by QT Designer.
    Two ways to use .ui file generated by Qt Designer.
    - Use .ui file directly by uic.loadUi('xxx.ui', self), 
      the Ui_Form parent is not needed in this case.
    - Use .py file generated by pyuic4, the Ui_Form parent
      is needed, investigate codes in the generated .py file
      to see why self.setupUi(self) is called.
    """

    def __init__(self):
        super(MagicBoxCentralWidget, self).__init__()
        # ALternative: Use .ui file - uic.loadUi('MagicBox.ui', self)
        self.setupUi(self)


def main(argv):
    app = QtGui.QApplication(argv)
    mb = MagicBoxGui()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)






