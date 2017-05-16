# coding: utf-8
import os
import pytest
from pyautomate import web

url = 'http://www.example.com'


@pytest.fixture
def webpage():
    if not os.path.exists('example_com.html'):
        web.download(url, 'example_com.html')
    yield 'example_com.html'
    os.unlink('example_com.html')


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
