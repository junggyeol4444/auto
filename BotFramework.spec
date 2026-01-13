# -*- mode: python ; coding: utf-8 -*-
"""
Bot Development Framework Suite - PyInstaller Spec File
Windows EXE 빌드 설정 파일
"""

block_cipher = None

# 분석할 메인 스크립트
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('bots', 'bots'),
        ('monitoring', 'monitoring'),
        ('analytics', 'analytics'),
        ('gui', 'gui'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'discord',
        'telegram',
        'linebot',
        'bs4',
        'selenium',
        'matplotlib',
        'reportlab',
        'pandas',
        'numpy',
        'requests',
        'aiohttp',
        'APScheduler',
        'PIL',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 불필요한 파일 제외
a.datas = [x for x in a.datas if not x[0].startswith('test')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BotFramework',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI 모드 (콘솔 창 숨김)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 아이콘 파일이 있다면: icon='icon.ico'
)
