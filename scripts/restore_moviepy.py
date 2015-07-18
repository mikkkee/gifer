"""Reset moviepy to its initial state."""

import os
import shutil


import moviepy

_base_dir = moviepy.__path__[0]

_platform = platform.platform()
_sliders_rel_path = 'video/io/sliders.py.backup'
_sliders_rel_path_original = 'video/io/sliders.py'
_video_all_rel_path = 'video/fx/all/__init__.py.backup'
_audio_all_rel_path = 'audio/fx/all/__init__.py.backup'
_video_all_rel_path_original = 'video/fx/all/__init__.py'
_audio_all_rel_path_original = 'audio/fx/all/__init__.py'

if _platform.startswith('Windows'):
    _sliders_rel_path = _sliders_rel_path.replace('/', '\\')
    _video_all_rel_path = _video_all_rel_path.replace('/', '\\')
    _audio_all_rel_path = _audio_all_rel_path.replace('/', '\\')
    _sliders_rel_path_original = _sliders_rel_path_original.replace('/', '\\')
    _video_all_rel_path_original = _video_all_rel_path_original.replace('/', '\\')
    _audio_all_rel_path_original = _audio_all_rel_path_original.replace('/', '\\')

_sliders_path = os.path.join(_base_dir, _sliders_rel_path)
_video_all_path = os.path.join(_base_dir, _video_all_rel_path)
_audio_all_path = os.path.join(_base_dir, _audio_all_rel_path)
_sliders_path_original = os.path.join(_base_dir, _sliders_rel_path_original)
_video_all_path_original = os.path.join(_base_dir, _video_all_rel_path_original)
_audio_all_path_original = os.path.join(_base_dir, _audio_all_rel_path_original)

shutil.move(_sliders_path, _sliders_path_original)
shutil.move(_video_all_path, _video_all_path_original)
shutil.move(_audio_all_path, _audio_all_path_original)