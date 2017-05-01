"""Generate spec file used by PyInstaller and build executable file
with it.
Todo: Add platform support for OS X and Linux"""
from __future__ import print_function
import os
import platform
from subprocess import call

import gifer

# If you have not modified MoviePy to get ready for PyInstaller, set
# __FRESH__ to True. Set __FRESH__ to False only if you have manually
# changed MoviePy using scripts/make_movie_py_static.py and
# scripts/rm_matplot_lib_dependency_in_moviepy.py .
__FRESH__ = True

__DEBUG__ = True # build using one-folder option of PyInstaller

ICON_PATH = 'images/logo_tray.ico'
ICON_PATH = ICON_PATH.replace( '/', '\\' ) if os.name == 'nt' else ICON_PATH
EXE_NAME  = 'gifer.exe' if os.name == 'nt' else 'gifer'
MODULES_TO_EXCLUDE = [
                        'Cython',
                        'IPython',
                        'PySide',
                        '_xmlplus',
                        'alabaster',
                        'astropy',
                        'babel',
                        'boto',
                        'bottleneck',
                        'bsddb',
                        'bz2',
                        'cdecimal',
                        'certifi',
                        'cffi',
                        'cryptography',
                        'cytoolz',
                        'docutils',
                        'elementtree',
                        'gevent',
                        'greenlet',
                        'h5py',
                        'lib2to3',
                        'lxml',
                        'matplotlib',
                        'openpyxl',
                        'pandas',
                        'pydoc',
                        'pytz',
                        'requests',
                        'scipy',
                        'skimage',
                        'sphinx',
                        'sqlalchemy',
                        'sqlite3',
                        'tabels',
                        'tcl',
                        'tkinter',
                        'tornado',
                        'win32sysloader',
                        'win32ui',
                        'zmq' ]


def write_spec_file( spec_name, debug=False ):
    """ Write build options to spec file. """
    lines = []

    exclude_line = 'modules_to_exclude = {}\n'.format( MODULES_TO_EXCLUDE )
    lines.append( exclude_line )

    unused_bin_lines = "def is_unused_binary( name ):\n" \
                       "    to_exclude = [ 'libeay32.dll' ]\n" \
                       "    if name.startswith( 'mkl' ):\n" \
                       "        if name.startswith( 'mkl_core' ) or name.startswith( 'mkl_intel_thread' ):\n" \
                       "            return False\n" \
                       "        return True\n" \
                       "    elif name in to_exclude:\n" \
                       "        return True\n" \
                       "    else:\n" \
                       "        return False\n"
    lines.append( unused_bin_lines )

    params_line = "block_cipher = None\n"
    lines.append( params_line )

    analysis_lines = [ "a = Analysis(['gifer.py'], ",
                         "pathex=['{gifer_dir}'], ",
                         "binaries=[],",
                         "datas=[],",
                         "hiddenimports=[],",
                         "hookspath=[],",
                         "runtime_hooks=[],",
                         "excludes=modules_to_exclude,",
                         "win_no_prefer_redirects=False,",
                         "win_private_assemblies=False,",
                         "cipher=block_cipher)\n", ]
    analysis_line = '\n'.join( analysis_lines )
    lines.append( analysis_line )

    binaries_lines = [ "a.binaries = a.binaries - TOC([",
        "('mfc90.dll', '', ''),",
        "('libmmd.dll', '', ''),",
        "('svml_dispmd.dll', '', ''),",
        "('sqlite3.dll', '', ''),",
        "('tcl85.dll', '', ''),",
        "('tk85.dll', '', ''),",
        "('_sqlite3', '', ''),",
        "('_tkinter', '', '')])\n",
        "a.binaries = [ x for x in a.binaries if not is_unused_binary( x[ 0 ] ) ]\n", ]
    binaries_line = '\n'.join( binaries_lines )
    lines.append( binaries_line )

    pyz_line = "pyz = PYZ( a.pure, a.zipped_data, cipher=block_cipher )\n"
    lines.append( pyz_line )

    if debug:
        exe_lines = [ "exe = EXE(pyz,",
                      "a.scripts,",
                      "exclude_binaries=True,",
                      "name='gifer',",
                      "debug=False,",
                      "strip=False,",
                      "upx=True,",
                      "console=True )\n", ]
        exe_line = '\n'.join( exe_lines )
        lines.append( exe_line )

        coll_lines = [ "COLLECT(exe,",
                       "a.binaries,",
                       "a.zipfiles,",
                       "a.datas,",
                       "strip=False,",
                       "upx=True,",
                       "name='gifer')\n", ]
        coll_line = '\n'.join( coll_lines )
        lines.append( coll_line )
    else:
        exe_lines = [ "exe = EXE(pyz,",
                      "a.scripts,",
                      "a.binaries,",
                      "a.zipfiles,",
                      "a.datas,",
                      "name='{}',".format( EXE_NAME ),
                      "debug=False,",
                      "strip=False,",
                      "upx=True,",
                      "console=False,",
                      "icon='{}' )\n".format( ICON_PATH ), ]
        exe_line = '\n'.join( exe_lines )
        lines.append( exe_line )

    with open( spec_name, 'w' ) as spec:
        spec.write( '\n'.join( lines ) )


def make_moviepy_static( ):
    """Turn runtime generated modules video.fx.all and audio.fx.all
    into static modules."""
    print( "Preparing MoviePy for building - video.fx.all/audio.fx.all." )
    script = 'scripts/make_moviepy_static.py'
    if platform.platform( ).startswith( 'Windows' ):
        script = script.replace( '/', '\\\\' )
    call( 'python {script}'.format( script=script ).split( ) )


def rm_matplotlib_dependency_in_moviepy( ):
    """Remove some unused files which have dependencies on MatPlotLib."""
    print( "Preparing MoviePy for building - MatPlotLib dependent files." )

    script = 'scripts/rm_matplot_lib_dependency_in_moviepy.py'
    if platform.platform( ).startswith( 'Windows' ):
        script = script.replace( '/', '\\\\' )
    call( 'python {script}'.format( script=script ).split( ) )


def restore_moviepy( ):
    """Restore changes made to MoviePy."""
    print( "Restore MoviePy changes." )

    script = 'scripts/restore_moviepy.py'
    if platform.platform( ).startswith( 'Windows' ):
        script = script.replace( '/', '\\\\' )
    call( 'python {script}'.format( script=script ).split( ) )


def build_exe( spec_file ):
    """ Build exe using PyInstaller and spec_file. """
    print( "Building executable." )
    call( 'pyinstaller {spec}'.format( spec=spec_file ).split( ) )


def main():
    global __FRESH__
    global __DEBUG__

    spec_file = 'build.spec'
    write_spec_file( spec_file, debug=__DEBUG__ )

    if __FRESH__:
        # MoviePy is fresh.
        make_moviepy_static( )
        rm_matplotlib_dependency_in_moviepy( )

    os.chdir( os.path.dirname( gifer.__file__ ) )
    build_exe( spec_file )

    if __FRESH__:
        restore_moviepy( )


if __name__ == '__main__':
    main()
