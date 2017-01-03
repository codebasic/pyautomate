from setuptools import setup

install_requires = [
    'pandas',
    'beautifulsoup4',
    'selenium',
    'requests',
    'python-docx',
]

setup(
    name='pyautomate',
    version='0.1',
    author='Lee Seongjoo',
    author_email='seongjoo@codebasic.io',
    description='Automate things',
    license='Apache 2.0',
    packages=['pyautomate'],
    install_requires=install_requires
)
