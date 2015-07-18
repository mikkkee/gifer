"""Generate spec file used by PyInstaller and build executable file
with it.
Todo: Add platform support for OS X and Linux"""
from __future__ import print_function
import os
import platform
from subprocess import call

import matplotlib as mpl

import gifer


# If you have not modified MoviePy to get ready for PyInstaller, set
# __FRESH__ to True. Set __FRESH__ to False only if you have manually
# changed MoviePy using scripts/make_movie_py_static.py and
# scripts/rm_matplot_lib_dependency_in_moviepy.py .
__FRESH__ = False

def write_spec_file(spec_name):
    """Write build options to spec file."""

    spec = open(spec_name, 'w')

    # Init Analysis() Object.
    _gifer_dir = os.path.dirname(gifer.__file__)

    spec.write(
        "a = Analysis(['gifer.py'],\n\
            pathex=['{gifer}'], \n\
            hiddenimports=[], hookspath=None, \n\
            runtime_hooks=None)\n\n".format(gifer=_gifer_dir)
    )

    # Modules to exclude.
    _ex_modules = ['PySide', 'IPython', 'matplotlib', 'scipy', 'pydoc', 'ssl']
    _ex_fmt = "a.binaries = \
[x for x in a.binaries if not x[0].startswith('{m}')]\n"

    for module in _ex_modules:
        spec.write(_ex_fmt.format(m=module))
    spec.write('\n')

    # Remove specific files.
    spec.write("""a.binaries = a.binaries - TOC([
        ('sqlite3.dll', '', ''),
        ('tcl85.dll', '', ''),
        ('tk85.dll', '', ''),
        ('_sqlite3', '', ''),
        ('_ssl', '', ''),
        ('_tkinter', '', '')])\n\n""")

    # Delete MatplotLib data
    _mpl_dir = os.path.dirname(mpl.__file__)
    _mpl_fmt = "a.datas = [x for x in a.datas if \
os.path.dirname(x[1]).startswith('{mpl_dir}')]\n\n"
    spec.write(_mpl_fmt.format(mpl_dir=_mpl_dir))

    # Write pyz / exe options
    spec.write('pyz = PYZ(a.pure)\n')
    _exe_fmt = "exe = EXE(pyz,\n\
        a.scripts,\n\
        a.binaries,\n\
        a.zipfiles,\n\
        a.datas,\n\
        name='{exe}',\n\
        debug=False,\n\
        strip=None,\n\
        upx=True,\n\
        console=False,\n\
        icon='{icon}')\n"

    _exe_name = 'gifer'
    _icon_path = 'images/logo_tray.ico'
    if platform.platform().startswith('Windows'):
        _exe_name += '.exe'
        _icon_path = _icon_path.replace('/', '\\')

    spec.write(_exe_fmt.format(exe=_exe_name, icon=_icon_path))

def make_moviepy_static():
    """Turn runtime generated modules video.fx.all and audio.fx.all
    into static modules."""
    print("Preparing MoviePy for building - video.fx.all/audio.fx.all.")
    script = 'scripts/make_moviepy_static.py'
    if platform.platform().startswith('Windows'):
        script = script.replace('/', '\\\\')
    call('python {script}'.format(script=script).split())

def rm_matplotlib_dependency_in_moviepy():
    """Remove some unused files which have dependencies on MatPlotLib."""
    print("Preparing MoviePy for building - MatPlotLib dependent files.")

    script = 'scripts/rm_matplot_lib_dependency_in_moviepy.py'
    if platform.platform().startswith('Windows'):
        script = script.replace('/', '\\\\')
    call('python {script}'.format(script=script).split())

def restore_moviepy():
    """Restore changes made to MoviePy."""
    print("Restore MoviePy changes.")

    script = 'scripts/restore_moviepy.py'
    if platform.platform().startswith('Windows'):
        script = script.replace('/', '\\\\')
    call('python {script}'.format(script=script).split())

def build_exe(spec_file):
    """Build exe using PyInstaller and spec_file."""
    print("Building executable.")
    call('pyinstaller {spec}'.format(spec=spec_file).split())


def main():
    global __FRESH__

    _spec_file = 'build.spec'
    write_spec_file(_spec_file)

    if __FRESH__:
        # MoviePy is fresh.
        make_moviepy_static()
        rm_matplotlib_dependency_in_moviepy()

    os.chdir(os.path.dirname(gifer.__file__))
    build_exe(_spec_file)

    if __FRESH__:
        restore_moviepy()


if __name__ == '__main__':
    main()

