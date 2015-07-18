"""Remove matplotlib dependency in some files of moviepy."""

import os
import shutil
import platform

import moviepy

_base_dir = moviepy.__path__[0]

_platform = platform.platform()
_io_rel_dir = 'video/io'

if _platform.startswith('Windows'):
    _io_rel_dir = _io_rel_dir.replace('/', '\\')

_io_dir = os.path.join(_base_dir, _io_rel_dir)

os.chdir(_io_dir)

shutil.move('sliders.py', 'sliders.py.backup')