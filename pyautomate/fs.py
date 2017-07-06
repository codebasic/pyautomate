# coding: utf-8

import os
from os.path import exists, join, isfile, isdir
from shutil import move
import shutil
import warnings

from send2trash import send2trash

from .__init__ import PathExistsWarning


def listdir(path='.', file_only=False, hidden=False, full_path=False):
    entry_list = []
    for entry in os.scandir(path):
        if entry.is_dir() and file_only:
            continue
        if entry.name.startswith('.') and not hidden:
            continue

        if full_path:
            entry_list.append(entry.path)
        else:
            entry_list.append(entry.name)
    return entry_list


def makedirs(name, exist_warning=False):
    if os.path.exists(name) and exist_warning:
        warnings.warn(name, PathExistsWarning)
    os.makedirs(name, exist_ok=True)
    return name


def touch(fname, mode=0o666, dir_fd=None, **kwargs):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(fname, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
        os.utime(
            f.fileno() if os.utime in os.supports_fd else fname,
            dir_fd=None if os.supports_fd else dir_fd, **kwargs)


def copy(src, target):
    if os.path.isfile(src):
        return shutil.copy2(src, target)
    elif os.path.isdir(src):
        return shutil.copytree(src, target)
    else:
        raise IOError('something wrong with {} or {}'.format(src, target))


def delete(path, ask=True):
    if not exists(path):
        return False

    confirm = True
    if ask:
        confirm = prompt_user('{} will be deleted. OK?'.format(path))
        if not confirm:
            return

    if isfile(path):
        return os.unlink(path)

    elif listdir(path):
        if ask:
            msg = '{} is not empty! Delete anyway?'
            confirm = prompt_user(msg.format(path))
        if not confirm:
            return
        return shutil.rmtree(path)
