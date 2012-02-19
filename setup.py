#!/usr/bin/env python

from distutils.core import setup

setup(name="mockaccino",
      version="0.1",
      description="Python library mock with an EasyMock flavor",
      author="Paolo Victor",
      author_email="paolovictor@gmail.com",
      url="http://github.com/paolovictor/mockaccino",
      license="MIT",
      packages=["mockaccino"],
      long_description=open("README.txt").read()
     )
