#!/usr/bin/env python

import os
import subprocess
import sys

from setuptools import find_packages, setup
from setuptools.command.develop import develop


TOP_PACKAGE_NAME = "PlottingNPCorr"


class CustomDevelopCommand(develop):
    """Custom handler for 'develop' command."""

    @staticmethod
    def _ensure_standalone_package_path(final_symlink_path):
        '''ensure that a dummy prefix path exists which is importable as a package'''

        _final_symlink_path_split = final_symlink_path.split('/')

        _cumulated_paths = ''
        for _i in range(len(_final_symlink_path_split)-1):
            _cumulated_path = os.path.join(*_final_symlink_path_split[:_i+1])
            # create directory
            if not os.path.exists(_cumulated_path):
                os.mkdir(_cumulated_path)
            # 'touch' __init__ file to ensure it exists
            _initfile_path = '{}/__init__.py'.format(_cumulated_path)
            if not os.path.exists(_initfile_path):
                open(_initfile_path, 'a').close()

        if not os.path.exists(final_symlink_path):
            os.symlink(os.path.join(*(['..']*(len(_final_symlink_path_split)-1)+['cfg/python'])), final_symlink_path)

    def run(self):
        print('custom_develop!')
        # create 'dummy' path with '__init__' files and symlink to '/python'
        self._ensure_standalone_package_path(TOP_PACKAGE_NAME+'/cfg')
        # call super
        develop.run(self)
        # 'touch' final __init__ file to ensure it exists
        _final_initfile_path = TOP_PACKAGE_NAME+'/cfg/__init__.py'
        if not os.path.exists(_final_initfile_path):
            open(_final_initfile_path, 'a').close()



def get_version():
    '''try to determine version via git'''
    try:
        # is git available?
        subprocess.call(['git', 'status'], stdout=subprocess.PIPE)
    except IOError:
        # 'git' not available
        version = "dev"
    except subprocess.CalledProcessError:
        # not a 'git' repo
        version = "dev"
    else:
        # 'git' found -> get release from git

        # is 'git describe' working
        try:
            # git describe working -> use output
            version = subprocess.check_output(['git', 'describe']).strip().decode()
        except subprocess.CalledProcessError:
            # git describe not working -> use commit hash
            version = 'git-' + subprocess.check_output(['git', 'log', '-1', '--format=%h']).strip().decode()

    return version


def get_requirements():
    _basic_requirements = [
        'NumPy',
        'Scipy',
        'matplotlib',
        'sphinx',
        'mock',
        'tqdm',
        'pandas',
        'PyYaml',
        'unittest2',
    ]

    if sys.version_info[0] == 2:
        _basic_requirements += ['enum']
    elif sys.version_info[0] == 3:
        _basic_requirements += []

    return _basic_requirements


setup(
    name=TOP_PACKAGE_NAME,
    version="dev",
    description='Toolset for calculating non-perturbative corrections with multithreading support. It is based on [Karma](https://github.com/dsavoiu/Karma).',
    author='Maximilian Horzela',
    author_email='maximilian.horzela@cern.ch',
    url='http://github.com/mhorzela/PlottingNPCorr',
    packages=['{}.cfg.{}'.format(TOP_PACKAGE_NAME, _pkg) for _pkg in find_packages('cfg/python')],
    package_dir = {
        TOP_PACKAGE_NAME+'.cfg': './cfg/python',
    },
    keywords = "mc data analysis cms cern",
    license='MIT',

    cmdclass={
        'develop': CustomDevelopCommand,
    },

 )
