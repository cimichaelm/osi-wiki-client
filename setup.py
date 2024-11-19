# filename: setup.py
# date: 2024-10-30
# version: 0.1
# author: AI Assistant

from setuptools import setup, find_packages

setup(
    name="xwikitools",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "xwikicli=xwikitools.xclicmd:main",
        ],
    },
)
