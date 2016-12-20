import sys

import pyinstaller_utils.dist

try:
    from distutils.core import setup as distutils_setup
except ImportError:
    from setuptools import setup as distutils_setup

from pyinstaller_utils.dist import build_exe
from pyinstaller_utils.windist import bdist_msi

# This file was originally taken from cx_Freeze by Anthony Tuininga, and is licensed under the  PSF license.

version = "5.0"
__version__ = version


def _AddCommandClass(commandClasses, name, cls):
    if name not in commandClasses:
        commandClasses[name] = cls


def setup(**attrs):
    commandClasses = attrs.setdefault("cmdclass", {})
    if sys.platform == "win32":
        if sys.version_info[:2] >= (2, 5):
            _AddCommandClass(commandClasses, "bdist_msi", bdist_msi)
    _AddCommandClass(commandClasses, "build_exe", build_exe)
    distutils_setup(**attrs)


pyinstaller_utils.dist.setup = setup  # Backwards compatibility
