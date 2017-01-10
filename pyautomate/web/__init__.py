# coding: utf-8
import os
import sys
import stat
import platform
import subprocess
import time
import urllib
from urllib.parse import urlparse
import re
import importlib
import warnings

import requests
import pip

from . import html
from ..__init__ import FileExistsWarning

def parse_html(src, encoding='utf-8'):
    """Returns BeautifulSoup from URL or file

    src: url or filepath
    encoding: (default=utf-8)
    """
    # check if url or filepath
    scheme = urlparse(src).scheme
    if re.compile('(http|https)').match(scheme):
        res = requests.get(src)
        doc = res.text
    else:
        doc = open(src, encoding=encoding)

    # select parser for BeautifulSoup
    # return BeautifulSoup(doc, parser)
    return html.Html(doc)

def download(url, filepath, chunksize=100000, overwrite=False):
    if os.path.exists(filepath) and not overwrite:
        return warnings.warn(FileExistsWarning(filepath, 'overwrite=True to overwrite'))

    res = requests.get(url)
    res.raise_for_status()

    with open(filepath, 'wb') as target_file:
        for chunk in res.iter_content(chunksize):
            if chunk:
                target_file.write(chunk)

def unquote_url(url):
    if '+' in url:
        return urllib.parse.unquote_plus(url)
    return urllib.parse.unquote(url)

def get_browser(driverpath, browser='Chrome'):
    from selenium import webdriver
    driver = getattr(webdriver, browser)(driverpath)
    return driver

def setup_webdriver(version, test=False):
    print('chromedriver 다운로드')
    downloaded_file = download_chromedriver(version)
    print(downloaded_file)

    # 압축 해제
    print('다운로드 받은 파일 압축 해제', end=' ... ')
    command_to_extract_zip = 'python -m zipfile -e {} .'.format(downloaded_file).split()
    subprocess.run(command_to_extract_zip, check=True)
    print('완료')

    # 실행권한 설정
    driverfile = 'chromedriver.exe' if platform.system() == 'Windows' else 'chromedriver'
    file_stat = os.stat(driverfile)
    os.chmod(driverfile, file_stat.st_mode | stat.S_IEXEC)

    if test:
        print('설정 테스트', end=' ... ')
        test_webdriver(driverfile)
        print('완료')

    return driverfile

def download_chromedriver(version):
    driverfile_map = {
        'Windows': 'chromedriver_win32.zip',
        'Darwin': 'chromedriver_mac64.zip'}
    download_target = driverfile_map.get(platform.system(), None)

    if download_target is None:
        sys.exit('No chromedriver for {0}'.format(platform.system()))

    chromedriver_url = 'http://chromedriver.storage.googleapis.com/'
    chromedriver_url += '{}/{}'.format(version, download_target)

    driverfilepath = download(chromedriver_url, download_target)
    return driverfilepath

def test_webdriver(driverfile):
    from selenium import webdriver
    chrome = webdriver.Chrome(os.path.join('.', driverfile))
    chrome.get('http://www.gogle.com')
    time.sleep(1)
    search_box = chrome.find_element_by_name('q')
    search_box.send_keys('파이썬')
    time.sleep(1)
    search_box.submit()
    time.sleep(1)
    chrome.quit()
