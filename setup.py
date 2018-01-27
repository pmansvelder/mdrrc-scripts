"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['menu.pyw']
DATA_FILES = ['mdrrc2_loclist.py', 'mdrrc2serial.py', 'mdrrcsettings.py']
OPTIONS = {'argv_emulation': True}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)