from distutils .core import setup
import py2exe
import glob

options = {"py2exe":{"dll_excludes":["MSVCP90.dll"]}}
setup(windows=[{"script":"RunFrame.py","icon_resources":[(1,"d:/Python/yuanchenglianjie/2.ico")]}],options=options,)