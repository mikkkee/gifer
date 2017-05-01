__author__ = 'Jianfeng'

import logging
import os
import re
import stat
import subprocess as sp
import sys

from PyQt4 import QtCore, QtGui
from imageio.core import InternetNotAllowedError, NeedDownloadError, get_platform, get_remote_file
from imageio.plugins.ffmpeg import FNAME_PER_PLATFORM

from resources.central_widget_ui import Ui_Form
import resources.icon


class Info( object ):
    """ Info object used to hold custom parameters to make GIF animation. """

    def __init__( self ):
        # Video name.
        self.video = None
        # Clip time.
        self.original_duration = None
        self.start             = None
        self.end               = None
        # Clip size.
        self.original_size = None
        self.width         = None
        self.height        = None
        self.scale         = None
        # Generate time symmetric GIF or not.
        self.mirrored      = False
        # Default GIF writing options.
        # fps - frames per second.
        # speed - change playing speed of the animation, default 1x.
        self.original_fps = None
        self.fps          = None
        self.speed        = 1

    @property
    def size( self ):
        """ GIF animation size. """
        return [ self.width, self.height ]

    def is_valid( self ):
        """
        Validate whether existing parameters are already enough to make a GIF animation.
        """
        return all( [ x is not None for x in [ self.video, self.start, self.end ] ] )

    def update_video( self, name ):
        """ Update the video to process. """
        assert isinstance( name, unicode )
        self.video = name

    def update_start( self, start=None ):
        """ Update clip starting time. """
        if start is not None:
            self.start = float( start )

    def update_end( self, end=None ):
        """ Update clip ending time. """
        if end is not None:
            self.end = float( end )

    def update_width( self, width=None ):
        """ Update clip resize width. """
        if width is not None:
            self.width = float( width )

    def update_height( self, height=None ):
        """ Update clip resize height. """
        if height is not None:
            self.height = float( height )

    def update_scale( self, scale=None ):
        """ Update clip resize scale. """
        if scale is not None:
            self.scale = float( scale )
        else:
            self.scale = None

    def update_fps( self, fps=None ):
        if fps:
            self.fps = float( fps )
        else:
            self.fps = None

    def update_speed( self, speed=None ):
        if speed:
            self.speed = float( speed )
        else:
            self.speed = None

    def update_mirror( self, mirrored=None ):
        if mirrored is not None:
            self.mirrored = mirrored


class ConsoleCapture( QtCore.QObject ):
    """Act as sys.stdout to capture console output.
    Here this Class is used to capture MoviePy output and show the message
    on status bar.
    """

    text_written = QtCore.pyqtSignal( str )
    text_content = ''

    def write( self, text ):
        self.text_content = self.text_content + text
        self.text_written.emit( self.text_content )

    def flush( self ):
        self.text_written.emit( self.text_content )


class MagicBox( object ):
    """ A magic box which can convert videos into GIF animations. """

    def __init__( self ):
        from moviepy.editor import VideoFileClip
        import moviepy.video.fx.all

        self.afx              = moviepy.video.fx.all
        self.VideoFileClipCls = VideoFileClip

        self.clip           = None
        self._original_clip = None
        self.info           = Info()

    def make_clip( self ):
        """ Customize clip according to parameters in self.info """
        # Init from video file.
        self.clip = self.VideoFileClipCls( self.info.video )
        # Create sub-clip.
        self.clip = self.clip.subclip( self.info.start, self.info.end )
        # Resize clip.
        if self.info.scale:
            self.clip = self.clip.resize( self.info.scale )
        else:
            self.clip = self.clip.resize( self.info.size )
        # Change play speed.
        if self.info.speed:
            self.clip = self.clip.speedx( self.info.speed )

    def save_gif( self, name ):
        """ Write VideoClip to a GIF file. """
        if self.info.mirrored:
            self.clip = self.afx.time_symmetrize( self.clip )
        self.clip.write_gif( name, fps=self.info.fps )


class MagicBoxGui( QtGui.QMainWindow ):
    """ GUI for MagicBox. """

    def __init__( self ):
        super( MagicBoxGui, self ).__init__()

        from moviepy.editor import VideoFileClip
        self.VideoFileClipCls = VideoFileClip

        # MagicBox() does all editing / writing things.
        self.magic_box      = MagicBox()
        # CentralWidget draw by QT Designer.
        self.central_widget = MagicBoxCentralWidget()
        # GIF to be loaded in the player.
        self.loaded_gif     = None
        # Last directory where user opened a video, default is current dir.
        self.last_video_dir = QtCore.QString()
        # Last directory where user saved a gif, default is current dir.
        self.last_gif_dir   = QtCore.QString()
        # Set window icon.
        self.setWindowIcon( QtGui.QIcon( ':/images/logo_tray.png' ) )

        self.init_ui( )

    def init_ui( self ):
        self.statusBar().showMessage( 'Ready' )
        self.setWindowTitle( 'GIFer' )

        # Menu bar - open video
        open_file = QtGui.QAction( 'Open Video', self )
        open_file.setShortcut( 'Ctrl+O' )
        open_file.setStatusTip( 'Open New Video' )
        open_file.triggered.connect( self.show_open_video_dialog )
        # Menu bar - open GIF
        open_gif = QtGui.QAction( 'Open GIF', self )
        open_gif.setShortcut( 'Ctrl+G' )
        open_gif.setStatusTip( 'Open New GIF Picture' )
        open_gif.triggered.connect( self.show_open_gif_dialog )
        # Menu bar - exit program
        exit_action = QtGui.QAction( '&Exit', self )
        exit_action.setShortcut( 'Ctrl+Q' )
        exit_action.setStatusTip( 'Exit application' )
        exit_action.triggered.connect( QtGui.qApp.quit )

        menu      = self.menuBar()
        file_menu = menu.addMenu( '&File' )
        file_menu.addAction( open_file )
        file_menu.addAction( open_gif )
        file_menu.addSeparator()
        file_menu.addAction( exit_action )

        ########### Setup central widget ##########

        # Validators.
        double_validator = QtGui.QDoubleValidator( self )
        double_validator.setBottom( 0 )

        self.central_widget.start_input.setValidator( double_validator )
        self.central_widget.end_input.setValidator(   double_validator )
        self.central_widget.width_input.setValidator( double_validator )
        self.central_widget.height_input.setValidator( double_validator )
        self.central_widget.fps_input.setValidator( double_validator )
        self.central_widget.scale_input.setValidator( double_validator )
        self.central_widget.speed_input.setValidator( double_validator )

        # Signals and slots.
        # LineEdits
        self.central_widget.start_input.textChanged.connect( self.handle_start_change )
        self.central_widget.end_input.textChanged.connect( self.handle_end_change )
        self.central_widget.width_input.textChanged.connect( self.handle_width_change )
        self.central_widget.height_input.textChanged.connect( self.handle_height_change )
        self.central_widget.scale_input.textChanged.connect( self.handle_scale_value_change )
        self.central_widget.fps_input.textChanged.connect( self.handle_fps_change )
        self.central_widget.speed_input.textChanged.connect( self.handle_speed_change )
        # Checkboxes
        self.central_widget.scale_check.stateChanged.connect( self.handle_scale_state_change )
        self.central_widget.mirror_check.stateChanged.connect( self.handle_mirrored_change )
        # PushButtons
        self.central_widget.video_file_btn.clicked.connect( self.show_open_video_dialog )
        self.central_widget.generate_btn.clicked.connect( self.generate_gif )
        self.central_widget.reset_btn.clicked.connect( self.reset_parameters )
        # GIF Player
        self.central_widget.play_btn.clicked.connect( self.play_loaded_gif )
        self.central_widget.pause_btn.clicked.connect( self.pause_loaded_gif )
        self.central_widget.stop_btn.clicked.connect( self.stop_loaded_gif )
        self.central_widget.next_frame_btn.clicked.connect( self.next_frame_loaded_gif )

        # Set initial state for widgets in central_widget.
        self.central_widget.video_file_input.setReadOnly( True )
        self.central_widget.scale_input.setDisabled( True )
        self.central_widget.gif_player.setAlignment( QtCore.Qt.AlignCenter )

        ############ Central Widget Setup Done ############

        # Attach central_widget to main window.
        self.setCentralWidget( self.central_widget )
        # Set initial position of main window.
        self.move( 100, 100 )

        self.show()

    def show_open_video_dialog( self ):
        """ Open video file to be processed. """
        # Default open directory is current directory.
        video_name = QtGui.QFileDialog.getOpenFileName( self, 'Open Video File', self.last_video_dir )
        video_name = unicode( video_name )

        if not video_name:
            # In case user closed open file dialog without doing anything.
            return

        # Update last_video_dir for next use.
        self.last_video_dir = QtCore.QString( os.path.dirname( video_name ) )

        # Update movie name in statusBar.
        msg = u'Selected: {name}'.format( name=video_name )
        self.statusBar().showMessage( msg )

        try:
            # Update video info, resolution, duration, fps, from VideoFileClip().
            self.magic_box.info.update_video( video_name )
            self.magic_box.clip = self.VideoFileClipCls( video_name )
            width, height = self.magic_box.clip.size
            duration = self.magic_box.clip.duration
            fps = self.magic_box.clip.fps

            self.magic_box.info.original_duration = duration
            self.magic_box.info.original_size = (width, height)
            self.magic_box.info.original_fps = fps

            # Update video info in main window.
            self.central_widget.video_file_input.setText( video_name )
            self.central_widget.start_input.setText( '0.0' )
            self.central_widget.end_input.setText( str( duration ) )
            self.central_widget.width_input.setText( str( width ) )
            self.central_widget.height_input.setText( str( height ) )
            self.central_widget.fps_input.setText( str( fps ) )
            self.central_widget.speed_input.setText( '1.0' )
        except UnicodeEncodeError:
            # Bug of Python 2.X on Windows, subprocess.call fails with unicode input.
            # See https://bugs.python.org/issue1759845 for more details.
            err_msg = u"Due to a Python 2.X bug on Windows, "\
                      u"unicode in file name {} is not supported".format( video_name )
            err_box = QtGui.QErrorMessage()
            err_box.showMessage( err_msg )
            self.statusBar().showMessage( None )

    def show_open_gif_dialog( self ):
        """Open GIF file and load it to GIF player."""
        gif_name = QtGui.QFileDialog.getOpenFileName( self, 'Open GIF File',
                                                      self.last_gif_dir, "GIF (*.gif)" )
        if gif_name:
            # In case user close dialog without opening any files.
            self.last_gif_dir = QtCore.QString( os.path.dirname( str( gif_name ) ) )
            self.load_gif( gif_name )

    def update_status_bar_gif_progress( self, text ):
        self.statusBar().showMessage( text )

    def reset_parameters( self ):
        """ Reset custom parameters, does not clear opened video. """
        if self.magic_box.info.video:
            # If there is video loaded, reset to video's parameters.
            self.central_widget.start_input.setText( '0.0' )
            self.central_widget.end_input.setText( str( self.magic_box.info.original_duration ) )

            self.central_widget.width_input.setText( str( self.magic_box.info.original_size[ 0 ] ) )
            self.central_widget.height_input.setText( str( self.magic_box.info.original_size[ 1 ] ) )

            self.central_widget.fps_input.setText( str( self.magic_box.info.original_fps ) )
            self.central_widget.speed_input.setText( '1.0' )
        else:
            # Reset to empty string if no video is opened.
            self.central_widget.start_input.setText( '' )
            self.central_widget.end_input.setText( '' )
            self.central_widget.width_input.setText( '' )
            self.central_widget.height_input.setText( '' )
            self.central_widget.fps_input.setText( '' )
            self.central_widget.speed_input.setText( '' )

        self.central_widget.scale_check.setCheckState( 0 )
        self.central_widget.mirror_check.setCheckState( 0 )

    def resizeEvent( self, event ):
        """ Customize the resizeEvent() inherited from QWidget. """
        super( MagicBoxGui, self ).resizeEvent( event )

        if self.loaded_gif:
            # Resize loaded_gif according to gif_player's size.
            size = self.central_widget.gif_player.size()
            self.resize_loaded_gif( size )

    def generate_gif( self ):
        """ Generate GIF animation using provided parameters. """
        if self.magic_box.info.is_valid():
            if self.loaded_gif:
                # Close opened gif.
                self.loaded_gif.setFileName( QtCore.QString() )

            self.magic_box.make_clip()
            gif_name = QtGui.QFileDialog.getSaveFileName( self, 'Save GIF File',
                                                          self.last_gif_dir, "GIF (*.gif)" )

            if gif_name:
                self.last_gif_dir = QtCore.QString( os.path.dirname( unicode( gif_name ) ) )
                self.magic_box.save_gif( unicode( gif_name ) )
                # Open GIF file after saved.
                self.load_gif( unicode( gif_name ) )

    def load_gif( self, gif_name ):
        """
        Load GIF file and fit its size to gif_player's size.
        GIF frame number is displayed in status bar.
        """
        self.loaded_gif = QtGui.QMovie()
        self.loaded_gif.setFileName( gif_name )

        player_size = self.central_widget.gif_player.size()
        self.central_widget.gif_player.setMovie( self.loaded_gif )

        self.loaded_gif.frameChanged.connect( self.update_status_bar_frame_number )

        self.loaded_gif.start()
        self.resize_loaded_gif( player_size )

    def resize_loaded_gif( self, size ):
        """
        Resize GIF to fit gif_player's size while keep its aspect ratio unchanged.
        """
        movie          = self.loaded_gif
        snapshot       = movie.currentImage()
        current_size   = snapshot.size()
        current_width  = float( current_size.width() )
        current_height = float( current_size.height() )
        screen_width   = float( size.width() )
        screen_height  = float( size.height() )

        if screen_height / screen_width > current_height / current_width:
            # Need to scale by screen width
            new_width  = int( screen_width )
            new_height = int( current_height * new_width / current_width )
        else:
            # Need to scale by screen height.
            new_height = int( screen_height )
            new_width  = int( current_width * new_height / current_height )
        movie.setScaledSize( QtCore.QSize( new_width, new_height ) )

    def update_status_bar_frame_number( self, frame ):
        """ Show GIF animation frame number in status bar. """
        # Frame number starts from 0.
        message = 'Frame: {frame}/{total_frame}'.format( frame=frame + 1,
                                                         total_frame=self.loaded_gif.frameCount() )
        self.statusBar().showMessage( message )

    def play_loaded_gif( self ):
        if self.loaded_gif:
            self.loaded_gif.start()

    def pause_loaded_gif( self ):
        if self.loaded_gif:
            self.loaded_gif.setPaused( True )

    def stop_loaded_gif( self ):
        if self.loaded_gif:
            self.loaded_gif.stop()

    def next_frame_loaded_gif( self ):
        if self.loaded_gif:
            self.loaded_gif.jumpToNextFrame()

    def handle_start_change( self, start ):
        """ Triggered when central_widget.start_input changes. """
        if start:
            self.magic_box.info.update_start( start )

    def handle_end_change( self, end ):
        """ Triggered when central_widget.end_input changes. """
        if end:
            self.magic_box.info.update_end( end )

    def handle_width_change( self, width ):
        """ Triggered when central_widget.width_input changes. """
        if width:
            self.magic_box.info.update_width( width )
            if not self.central_widget.height_input.text() and self.magic_box.info.video:
                # Update height if its input is empty and there is video opened
                height = float( width ) / self.magic_box.info.original_size[ 0 ] \
                         * self.magic_box.info.original_size[ 1 ]
                self.central_widget.height_input.setText( str( height ) )

    def handle_height_change( self, height ):
        """ Triggered when central_widget.height_input changes. """
        if height:
            self.magic_box.info.update_height( height )
            if not self.central_widget.width_input.text() and \
                    self.magic_box.info.video:
                # Update width if its input is empty and there is video opened
                width = float( height ) / self.magic_box.info.original_size[ 1 ] \
                        * self.magic_box.info.original_size[ 0 ]
                self.central_widget.width_input.setText( str( width ) )

    def handle_scale_state_change( self, scale_state ):
        """ Triggered when central_widget.scale_check changes. """
        scaled = bool( scale_state )

        self.central_widget.width_input.setDisabled( scaled )
        self.central_widget.height_input.setDisabled( scaled )
        self.central_widget.scale_input.setDisabled( not scaled )

        if scaled and self.magic_box.info.video:
            width, height = self.magic_box.info.original_size
            self.central_widget.width_input.setText( str( width ) )
            self.central_widget.height_input.setText( str( height ) )
        else:
            # Set scale in Info() to None.
            self.magic_box.info.update_scale( None )

    def handle_scale_value_change( self, scale_ratio ):
        """ Triggered when central_widget.start_value changes. """
        ratio = float( scale_ratio )

        self.magic_box.info.update_scale( ratio )

        width  = ratio * self.magic_box.info.original_size[ 0 ]
        height = ratio * self.magic_box.info.original_size[ 1 ]
        self.central_widget.width_input.setText( str( width ) )
        self.central_widget.height_input.setText( str( height ) )

    def handle_fps_change( self, fps ):
        """ Triggered when central_widget.fps_input changes. """
        if fps:
            self.magic_box.info.update_fps( fps )

    def handle_speed_change( self, speed ):
        """ Triggered when central_widget.speed_input changes. """
        if speed:
            self.magic_box.info.update_speed( speed )

    def handle_mirrored_change( self, mirrored ):
        """ Triggered when central_widget.mirror_check changes. """
        if mirrored:
            self.magic_box.info.update_mirror( True )
        else:
            self.magic_box.info.update_mirror( False )


class MagicBoxCentralWidget( QtGui.QWidget, Ui_Form ):
    """
    Central widget draw by QT Designer.

    Two ways to use .ui file generated by Qt Designer.
    - Use .ui file directly by call uic.loadUi('xxx.ui', self) in constructor, the Ui_Form parent is not needed
      in this case.
    - Use .py file generated by pyuic4, the Ui_Form parent is needed, investigate code in the generated .py file
      to see why self.setupUi(self) is called.
    """

    def __init__( self ):
        super( MagicBoxCentralWidget, self ).__init__()
        # ALternative: Use .ui file - uic.loadUi('central_widget.ui', self)
        self.setupUi( self )


class DownloadInfoCapturer( QtCore.QObject ):
    """
    Capture download info from stdout.
    Need to redirect sys.stdout to this object to enable capturing.
    """

    text_written  = QtCore.pyqtSignal( unicode )
    _text_content = ''
    percent       = ''

    def text_content( self ):
        """" Return the text to be emitted """
        if self.percent:
            return ( self._text_content + '\n{}' ).format( self.percent )
        else:
            return self._text_content

    def write( self, text ):
        """ Replacement for stdout.write """
        percent_pattern = r'(\(\d{1,3}\.\d%\))'
        self.percent    = re.search( percent_pattern, text )

        if self.percent:
            self.percent = self.percent.group()[ 1:-1 ]
        else:
            self.percent = ''

            if not self._text_content.endswith( '\n' ):
                self._text_content = '\n'.join( [ self.text_content(), text ] )
            else:
                self._text_content = self._text_content + text

        self.text_written.emit( self.text_content() )

    def flush( self ):
        """ Replacement for stdout.flush """
        self.text_written.emit( self.text_content() )


class DownloadThread( QtCore.QThread ):
    """ A QThread to manage download of ffmpeg """

    def __int__(self):
        QtCore.QThread.__init__( self )

    def run( self ):
        import sys
        output     = DownloadInfoCapturer( text_written=self.update_info )
        sys.stdout = output
        find_ffmpeg( auto=True )
        self.emit( QtCore.SIGNAL( 'downloadFinished' ) )

    def update_info( self, text ):
        self.emit( QtCore.SIGNAL( 'hasOutput' ), text )

    def __del__(self):
        sys.stdout = sys.__stdout__


class PreStartingWidget( QtGui.QWidget ):
    """ A widget that shows up when ffmpeg is not found in user's system """

    def __init__( self, info ):
        super( self.__class__, self ).__init__()

        label_msg = 'ffmpeg is not found in your system.\n'\
                    'GIFer will not work without ffmpeg.\n' \
                    'Do you want GIFer to download it for you (from github.com)?\n'

        font = QtGui.QFont()
        font.setPointSize( 10 )

        self.label = QtGui.QTextEdit()
        self.label.setReadOnly( True )
        self.label.setAlignment( QtCore.Qt.AlignVCenter )
        self.label.setText( label_msg )
        self.label.setFont( font )

        self.yes_btn = QtGui.QPushButton( 'YES' )
        self.no_btn  = QtGui.QPushButton( 'NO' )

        self.yes_btn.clicked.connect( self.download_ffmpeg )
        self.no_btn.clicked.connect( self.close )

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget( self.label )
        vbox.addWidget( self.yes_btn )
        vbox.addWidget( self.no_btn )

        self.setLayout( vbox )
        self.setWindowTitle( info )
        self.resize( 500, 400 )

        self.thread = DownloadThread()
        self.connect( self.thread, QtCore.SIGNAL( 'hasOutput' ), self.label.setText )
        self.connect( self.thread, QtCore.SIGNAL( 'downloadFinished' ), self.download_finished )

    def download_ffmpeg(self):
        self.setWindowTitle( 'GIFer - Downloading ffmpeg for you' )
        self.label.setText( 'Downloading' )
        self.thread.start()

    def download_finished(self):
        alert = QtGui.QMessageBox()
        alert.setText( 'ffmpeg downloaded. Please restart GIFer.' )
        alert.setWindowTitle( 'Download Finished' )
        alert.buttonClicked.connect( self.close )
        self.setDisabled( True )
        alert.exec_()

    def __del__(self):
        sys.stdout = sys.__stdout__


def find_ffmpeg( auto=False ):
    """ Get ffmpeg exe, modified from imageio.plugins.ffmpeg.get_exe """
    # Is the ffmpeg exe overridden?
    exe = os.getenv( 'IMAGEIO_FFMPEG_EXE', None )
    if exe:  # pragma: no cover
        return exe

    # Check if ffmpeg is in PATH
    try:
        with open( os.devnull, "w" ) as null:
            sp.check_call( [ "ffmpeg", "-version" ], stdout=null,
                           stderr=sp.STDOUT )
            return "ffmpeg"
    # ValueError is raised on failure on OS X through Python 2.7.11
    # https://bugs.python.org/issue26083
    except (OSError, ValueError, sp.CalledProcessError):
        pass

    plat = get_platform( )

    if plat and plat in FNAME_PER_PLATFORM:
        try:
            exe = get_remote_file( 'ffmpeg/' + FNAME_PER_PLATFORM[ plat ],
                                   auto=auto )
            os.chmod( exe, os.stat( exe ).st_mode | stat.S_IEXEC )  # executable
            return exe
        except NeedDownloadError:
            raise NeedDownloadError( 'Need ffmpeg exe. '
                                     'You can download it by calling:\n'
                                     '  imageio.plugins.ffmpeg.download()' )
        except InternetNotAllowedError:
            pass  # explicitly disallowed by user
        except OSError as err:  # pragma: no cover
            logging.warning( "Warning: could not find imageio's "
                             "ffmpeg executable:\n%s" %
                             str( err ) )

    # Fallback, let's hope the system has ffmpeg
    return 'ffmpeg'


def main( argv ):
    app = QtGui.QApplication( argv )

    try:
        find_ffmpeg( auto=False )
        mb = MagicBoxGui( )
    except NeedDownloadError:
        info_box = PreStartingWidget( 'Checking ffmpeg on your system' )
        info_box.show()

    sys.exit( app.exec_() )


if __name__ == '__main__':
    main( sys.argv )
