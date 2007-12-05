#!/usr/bin/env python

from setuptools import setup, find_packages
import os

root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

setup(
    name = "Serpantin",
    version = __import__('serpantin').VERSION,
    packages = find_packages(),
    include_package_data = True,

    # metadata for upload to PyPI
    author = "Serpantin Project",
    author_email = "info@dial.com.ru",
    description = "Small ERP application built with django and dojo",
    license = "BSD",
    keywords = "python django dojo ERP application",
    url = "http://code.google.com/p/serpantin/", # project home page, if any
)
