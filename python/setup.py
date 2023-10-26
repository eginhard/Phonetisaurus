#!/usr/bin/python
from setuptools import setup, find_packages

#Install phonetisaurus
setup (
    name         = 'phonetisaurus-bindings',
    version      = '0.3.2',
    description  = 'Phonetisaurus G2P python package (OpenFst-1.6.x)',
    url          = 'http://code.google.com/p/phonetisaurus',
    author       = 'Josef Novak',
    author_email = 'josef.robert.novak@gmail.com',
    license      = 'BSD',
    packages=find_packages(),
    package_data={"phonetisaurus": ["Phonetisaurus.so"]},
    include_package_data = True,
    install_requires = ["argparse", "bottle"],
    zip_safe     = False
)
