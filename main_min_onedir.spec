# -*- mode: python -*-
import os
import matplotlib

a = Analysis(['gifer.py'],
             pathex=['D:\\Google Drive\\Coding\\gifer'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

a.binaries = [x for x in a.binaries if not x[0].startswith('PySide')]
a.binaries = [x for x in a.binaries if not x[0].startswith('IPython')]
a.binaries = [x for x in a.binaries if not x[0].startswith('matplotlib')]
a.binaries = [x for x in a.binaries if not x[0].startswith('scipy')]
a.binaries = [x for x in a.binaries if not x[0].startswith('pydoc')]
a.binaries = [x for x in a.binaries if not x[0].startswith('ssl')]

# Target remove specific ones...
a.binaries = a.binaries - TOC([
 ('sqlite3.dll', '', ''),
 ('tcl85.dll', '', ''),
 ('tk85.dll', '', ''),
 ('_sqlite3', '', ''),
 ('_ssl', '', ''),
 ('_tkinter', '', '')])

# Delete everything bar matplotlib data...
_matplotlib_path = os.path.dirname(matplotlib.__file__)
a.datas = [x for x in a.datas if
 os.path.dirname(x[1]).startswith(_matplotlib_path)]
 
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='main',
               icon='images\\logo_tray.ico')
