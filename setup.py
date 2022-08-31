import sys
from cx_Freeze import setup, Executable

base = None
# if sys.platform == 'win32':
#     base = 'Win32GUI'

exe = Executable(
    script="main_exe.py",
    base=base,
    target_name='Photo Sorter' if sys.platform == 'Linux' else "Photo Sorter.exe",
    icon='data/tri.ico'
    )

setup(
    name = "Photos Sorter",
    version = "0.1",
    description = "Automatically sort your photos into directories based on time in exif data.",
    author="Sheepolata",
    url="https://github.com/sheepolata/photosorterlib",
    executables = [exe]
)
