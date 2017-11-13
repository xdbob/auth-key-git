import os
from setuptools import setup

setup(
    name = "auth_key_git",
    version = "0.1",
    description = "ssh keys via ldap",
    packages = ['auth_key_git'],
    entry_points = {
        'console_scripts': ['auth_key_git = auth_key_git.__init__:main']
    },
    install_requires=[
            'pyldap',
            'configparser',
    ]
)
