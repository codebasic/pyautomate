from setuptools import setup

install_requires = [
    'pandas',
    'beautifulsoup4',
    'selenium',
    'requests',
    'python-docx',
    'python-pptx',
    'pdfminer.six'
]

setup(
    name='pyautomate',
    version='0.1.1',
    author='Lee Seongjoo',
    author_email='seongjoo@codebasic.io',
    description='Automate things',
    license='Apache 2.0',
    packages=['pyautomate', 'pyautomate.office', 'pyautomate.web'],
    install_requires=install_requires
)
