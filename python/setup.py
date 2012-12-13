#!/usr/bin/env python
import os

__version__ = '0.1.1'
VERSION = tuple(map(int, __version__.split('.')))

try:
    from Cython.Distutils import build_ext
    have_cython = 1
except ImportError:
    have_cython = 0

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

#f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
#long_description = f.read()
#f.close()

src_files = []
if have_cython:
    src_files.append('okapi/okapi_bss.pyx')
    cmdclass = {'build_ext': build_ext}
else:
    src_files.append('okapi/okapi_bss.c')
    cmdclass = {}

ext_modules = [Extension("okapi", src_files,
				libraries=['okapibss'])]


setup(
    name='okapi',
    version=__version__,
    description='Python client for Okapi IR system',
    #long_description=long_description,
    url='http://github.com/ncloudioj/okapi',
    author='Nan Jiang',
    author_email='njiang028@gmail.com',
    maintainer='Nan Jiang',
    maintainer_email='njiang028@gmail.com',
    keywords=['Okapi', 'Information Retrieval'],
    license='BSD',
    ext_modules=ext_modules,
	cmdclass = cmdclass,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        ]
)
