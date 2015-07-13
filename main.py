__author__ = 'Jianfeng'


from moviepy.editor import *


class Info(object):
    """Info object used to hold user inputs"""

    def __init__(self):
        self.start = None
        self.end = None
        self.top_left = ()
        self.bottom_right = ()
        self.mirrored = False
        self.video = None


class MagicBox(object):
    """A magic box which can convert videos into gif pictures."""

    def __init__(self):
        self.video = None
        self.clip = None
        self._original_clip = None
        self.info = Info()

    def add_video(self, video_name):
        self.video = video_name
        self.info.video = video_name

    def set_clip_time(self, start, end):
        """Change starting, ending time of clip.
        Update changes in info.
        """
        self.clip = self._original_clip.subclip(start, end)
        self.info.start, self.info.end = start, end

    def set_clip_size(self, top_left, bottom_right):
        """Change clip size.
        By providing two lists/tuples indicating (x, y) coordinates
        of top left and bottom right corners.
        """
        pass


