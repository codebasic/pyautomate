import os
import shutil
import subprocess

def prompt_user(message):
    prompt = input('{} (y/n) '.format(message))
    return True if prompt.lower().startswith('y') else False

def touch(filepath, content=None, overwrite=True, encoding='utf-8'):
    mode = 'w' if overwrite else 'a'
    with open(filepath, mode, encoding=encoding) as file:
        if content:
            file.write(content)

    return filepath

def print_file(path, nlines=5, encoding='utf-8'):
    with open(path, encoding=encoding) as file:
        for line in file:
            print(line.rstrip())

def delete_path(path, ask=True):
    if not os.path.exists(path):
        return print('{} does not exist'.format(path))

    confirm = True
    if ask:
        confirm = prompt_user('{} will be deleted. OK?'.format(path))
        if not confirm:
            return

    if os.path.isfile(path):
        return os.unlink(path)

    elif os.listdir(path):
        if ask:
            confirm = prompt_user('{} is not empty! Delete anyway?'.format(path))
        if not confirm:
            return
        return shutil.rmtree(path)

def zipit(output, files, option='c'):
    command = 'python -m zipfile'
    command = '{} -{} {}'.format(command, option, output)
    command = '{} {}'.format(
        command, ' '.join(files))
        #command, ' '.join(map(lambda fn: '"{}"'.format(fn), files)))
    result = subprocess.run(command.split())
    result.check_returncode()
