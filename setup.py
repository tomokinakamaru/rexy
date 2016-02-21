# coding:utf-8

from setuptools import setup, find_packages

long_description = """\
"""

setup(
    author='Tomoki Nakamaru',
    author_email='tomoki.nakamaru@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    description='',
    install_requires=[
        'wexy==1.0.0'
    ],
    license='MIT',
    long_description=long_description,
    name='rexy',
    packages=find_packages(),
    platforms='any',
    url='http://github.com/tomokinakamaru/rexy',
    version='1.0.0'
)
