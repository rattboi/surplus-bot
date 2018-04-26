#!/usr/bin/env python
from setuptools import setup

setup(
    name="PDX Surplus Bot",
    version="0.1.0",
    author="Bradon Kanyid",
    author_email="bradon@kanyid.org",
    description=("Post about new listings on PDX.edu surplus page"),
    license="MIT",
    install_requires=[
        'requests',
        'beautifulsoup4',
        'arrow',
    ],
    entry_points="""\
    [console_scripts]
    surplus_bot = surplus.surplus:cli
    """,
)
