import sys

if sys.version_info >= (3, 4):
    from contextlib import suppress
else:
    from contextlib2 import suppress

from PyInstaller.building.makespec import main as makespec_main
import inspect
import uuid
import os
import distutils
import deepmerge

entry_keys = [
    'console_scripts',
    'gui_scripts',
]

excluded_args = [
    'scripts',
    'specpath',
]


def merge_defaults(a, b):
    merger = deepmerge.Merger(
        # pass in a list of tuple, with the
        # strategies you are looking to apply
        # to each type.
        [(list, ["append"]), (dict, ["merge"])],
        # next, choose the fallback strategies,
        # applied to all other types:
        ["override"],
        # finally, choose the strategies in
        # the case where the types conflict:
        ["override"])

    merger.merge(a, b)
    return a


def makespec_args():
    names = ['datas']  # signature does not detect datas for some reason
    for name, parameter in inspect.signature(makespec_main).parameters.items():
        if name not in (excluded_args + ['args', 'kwargs']):
            names.append(name)

    return names


def decode(bytes_or_string):
    if isinstance(bytes_or_string, bytes):
        return bytes_or_string.decode()
    else:
        return bytes_or_string


def is_binary(file):
    return file.endswith(('.so', '.pyd', '.dll', ))


def rename_script(executable):
    # Per issue #32.
    new_script_name = '{}.{}.py'.format(executable.script, str(uuid.uuid4()))
    os.rename(executable.script, new_script_name)
    executable.script = new_script_name


def build_dir():
    return "exe.{}-{}".format(distutils.util.get_platform(), sys.version[0:3])


def move_tree(source, destination):
    if not os.path.exists(destination):
        return False
    for path, dirs, files in os.walk(source):
        relPath = os.path.relpath(path, source)
        destPath = os.path.join(destination, relPath)
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        for file in files:
            destFile = os.path.join(destPath, file)
            if os.path.isfile(destFile):
                continue
            srcFile = os.path.join(path, file)
            os.rename(srcFile, destFile)
    for path, dirs, files in os.walk(source, False):
        if len(files) == 0 and len(dirs) == 0:
            os.rmdir(path)
