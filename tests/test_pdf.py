# coding: utf-8
import os
import pytest

from pyautomate.pdf import PDFDocument


@pytest.fixture
def data():
    data_dir, filename = os.path.split(__file__)
    test_dir, _ = os.path.splitext(filename)
    test_dir = os.path.join(data_dir, test_dir)
    print(test_dir)
    pdf_files = os.listdir(test_dir)
    pdf_files = [os.path.join(test_dir, fn) for fn in pdf_files]
    return pdf_files


def test_pdf(data):
    for filename in data:
        doc = PDFDocument(filename)
        assert hasattr(doc, 'extract_text')
        assert doc.extract_text()
