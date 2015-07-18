"""MoviePy dynamicly generates moviepy.video.fx.all and moviepy.audio.fx.all 
module based on files in parent directory. This will cause import error when
moviepy is packed by pyinstaller. This script generates static __init__.py
files in moviepy/video/fx/all and moviepy/audio/fx/all to eliminate this kind
of errors.
"""

import os
import shutil
import platform

import moviepy

_base_dir = moviepy.__path__[0]

_platform = platform.platform()
_video_all_rel_dir = 'video/fx/all'
_audio_all_rel_dir = 'audio/fx/all'

if _platform.startswith('Windows'):
    _video_all_rel_dir = _video_all_rel_dir.replace('/', '\\')
    _audio_all_rel_dir = _audio_all_rel_dir.replace('/', '\\')

_video_all_dir = os.path.join(_base_dir, _video_all_rel_dir)
_audio_all_dir = os.path.join(_base_dir, _audio_all_rel_dir)

for _cur_dir in [_video_all_dir, _audio_all_dir]:
    os.chdir(_cur_dir)

    shutil.copy('__init__.py', '__init__py.backup')

    _directory = os.path.dirname(
                    os.path.dirname(
                        os.path.realpath(__file__)))

    _files = os.listdir(_directory)
    _fx_list = [_f for _f in _files if ( _f.endswith('.py') and
                                    not _f.startswith('_'))]

    __all__ = [_c[:-3] for _c in _fx_list]

    with open('__init__.py', 'w') as init_file:
        fmt = 'from ..{x} import {y}\n'
        for _name in __all__:
            init_file.write(fmt.format(x=_name, y=_name))