import os
import pytest

from pyautomate import fs


def test_listdir():
    fs.touch('.hidden')

    entry_list = fs.listdir()
    for entry in entry_list:
        if entry.startswith('.'):
            error_msg = 'Hidden entries should not be included: {}'
            assert False, error_msg.format(entry)

    error_msg = 'Hidden entries should be included'
    assert fs.listdir(hidden=True) == os.listdir(), error_msg

    error_msg = 'Only files should be include'
    dir_entry_list = []
    for entry in fs.listdir(file_only=True):
        if os.path.isdir(entry):
            dir_entry_list.append(entry)
    assert not dir_entry_list, error_msg

    error_msg = 'Should be full path'
    dirpath = 'sandbox'
    if not os.path.exists('sandbox'):
        os.makedirs('sandbox')

    fs.touch('sandbox/empty.txt')
    fs.touch('sandbox/.hidden')

    for entry in fs.listdir(dirpath, full_path=True):
        dirname, basename = os.path.split(entry)
        assert dirname == dirpath, error_msg


def test_makedirs():
    dirname = 'sandbox'
    # create path
    fs.makedirs(dirname)
    assert os.path.exists(dirname)
    # check if no exceptions raised
    fs.makedirs(dirname)


def test_zip():
    dirname = 'attachment'
    fs.makedirs(dirname)
    fs.touch(fs.join(dirname, '보고서.docx'))
    fs.touch(fs.join(dirname, '데이터.csv'))
    fs.touch(fs.join('요약.xlsx'))

    fs.zip('첨부파일.zip', dirname)
    assert fs.exists('첨부파일.zip')
    fs.zip('첨부파일2', dirname)
    assert fs.exists('첨부파일2.zip')

    fs.delete('첨부파일.zip')
    fs.delete('첨부파일2.zip')


def test_unzip():
    dirname = 'attachment'
    fs.makedirs(dirname)
    fs.touch(fs.join(dirname, '보고서.docx'))
    fs.touch(fs.join(dirname, '데이터.csv'))
    fs.touch(fs.join(dirname, '요약.xlsx'))
    fs.zip('첨부파일.zip', dirname)

    fs.unzip('첨부파일.zip')
    expected = ['보고서.docx', '데이터.csv', '요약.xlsx']
    assert sorted(fs.listdir('attachment')) == sorted(expected)
    fs.unzip('첨부파일.zip', '첨부파일')
    expected2 = [path.join('attachment', e) for e in expected]
    assert sorted(fs.listdir('첨부파일')) == sorted(expected2)
