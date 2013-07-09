#!/usr/bin/env python

from setuptools import setup, find_packages
import glob
import subprocess
import os

def walk_topdirs(dest, topdirs):
    # dest: where to store the walked files e.g. 'share/rhui-testing-tools'
    # topdirs: what to walk e.g. ['testing-data', 'rhui-tests', ...]
    datafiles = []
    for topdir in topdirs:
        for dirname, dirnames, filenames in os.walk(topdir):
            datafiles.append(
                (
                    os.path.join(dest, dirname),
                    map(lambda x: os.path.join(dirname, x), filenames)
                )
            )
    return datafiles

datafiles = [('share/splice-testing-tools/spacewalk-report-mock', ['spacewalk-report-mock/common.py'])]

for topdir in glob.glob('spacewalk-report-mock/test*'):
    for dirname, dirnames, filenames in os.walk(topdir):
        datafiles.append(('share/splice-testing-tools/' + dirname, map(lambda x: dirname + "/" + x, [fn for fn in filenames if fn.endswith(".py") or fn.endswith(".yaml") or fn.endswith(".md")])))

setup(name='splicetestlib',
    version='0.2',
    description='Splice Testing library',
    author='Vitaly Kuznetsov',
    author_email='vitty@redhat.com',
    url='https://github.com/RedHatQE/splice-testing-tools',
    license="GPLv3+",
    packages=find_packages(exclude=['*.pyc', '*.swp']),
    data_files=datafiles + \
        walk_topdirs('share/splice-testing-tools', ['splice-tests']) + \
        walk_topdirs('/usr', ['lib/systemd']) + \
        walk_topdirs('/', ['etc']),
    classifiers=[
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Operating System :: POSIX',
            'Intended Audience :: Developers',
            'Development Status :: 4 - Beta'
    ],
    entry_points = {
        'nose.plugins.0.10': [
            'webui_screenshot = pageobjects.nose_plugins.webui_screenshot:Webui_screenshot'
            ]
        },
    scripts=glob.glob('scripts/*')
)
