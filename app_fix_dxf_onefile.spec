# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['app_fix_dxf.py'],
             pathex=['C:\\Users\\baidak\\acad_py_scripts\\app_fix_dxf'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [('logo_ug.png', 'C:\\Users\\baidak\\acad_py_scripts\\app_fix_dxf\\logo_ug.png', 'Data')]

for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='Ремонт dxf',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
