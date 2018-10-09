#!/usr/bin/env python
import re
import sys
import os

from setuptools import setup


with open("README.rst") as fp:
    long_desc = fp.read()

setup(
    name="StormSpans",
    version="1.0.0",
    description=
        "PostgreSQL range type support for Canonical's Storm ORM using Spans ",
    long_description=long_desc,
    license="MIT",
    author="Andreas Runfalk",
    author_email="andreas@runfalk.se",
    url="https://www.github.com/runfalk/stormspans",
    packages=["stormspans"],
    install_requires=[
        "spans",
        "psycospans",
    ],
    extras_require={
        "dev": [
            "psycopg2-binary",
            "pytest",
            "storm-legacy",
        ],
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends"
    ),
    zip_safe=False,
    test_suite="stormspans.tests.test_suite"
)
