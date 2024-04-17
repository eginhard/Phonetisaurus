#!/usr/bin/python
from setuptools import setup, find_packages

with open("../README.md") as f:
    README = f.read()

#Install phonetisaurus
setup (
    name         = "phonetisaurus-bindings",
    version      = "0.3.2",
    description  = "Phonetisaurus G2P python package (OpenFst-1.7.2)",
    long_description=README,
    long_description_content_type="text/markdown",
    url          = "https://github.com/eginhard/phonetisaurus",
    author       = "Josef Novak",
    author_email = "josef.robert.novak@gmail.com",
    maintainer   = "Enno Hermann",
    maintainer_email="enno.hermann@gmail.com",
    license      = "BSD",
    packages=find_packages(),
    package_data={"phonetisaurus": ["Phonetisaurus.so"]},
    install_requires = ["argparse", "bottle"],
    zip_safe     = False,
    python_requires=">=3.6.0",
    project_urls={
        "Repository": "https://github.com/eginhard/phonetisaurus",
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
