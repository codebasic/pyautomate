# coding: utf-8
import os
import platform
import time
import pytest
from pyautomate import web

url = 'http://www.example.com'


@pytest.fixture
def webpage():
    if not os.path.exists('example_com.html'):
        web.download(url, 'example_com.html')
    yield 'example_com.html'
    os.unlink('example_com.html')


@pytest.fixture
def driverfile():
    filepath = 'chromedriver'
    if platform.system() == 'Windows':
        filepath += '.exe'
    return filepath


def test_parse_html():
    assert web.parse_html(url)
    if not os.path.exists('example_com.html'):
        web.download(url, 'example_com.html')
    assert web.parse_html('example_com.html')

    html = open('example_com.html', encoding='utf8').read()
    assert web.parse_html(html)

    with pytest.raises(ValueError):
        web.parse_html([])


def test_html(webpage):
    html = web.parse_html(webpage)
    assert html
    assert html.title.text == 'Example Domain'


def test_setup_webdriver():
    web.setup_webdriver(2.26)

    driverfile = 'chromedriver'
    if platform.system() == 'Windows':
        driverfile += '.exe'

    error_msg = 'chromedriver file does not exist.'
    assert os.path.exists(driverfile), error_msg


def test_webdriver(driverfile):
    from selenium import webdriver
    chrome = webdriver.Chrome(os.path.join('.', driverfile))

    try:
        chrome.get('http://www.gogle.com')
        time.sleep(1)
        search_box = chrome.find_element_by_name('q')
        search_box.send_keys('파이썬')
        time.sleep(1)
        search_box.submit()
        time.sleep(1)
    finally:
        chrome.quit()
