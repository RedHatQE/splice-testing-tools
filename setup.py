#!/usr/bin/env python

from setuptools import setup
import glob
import subprocess
import os

datafiles = []
for test in glob.glob('spacewalk-report-mock/test*/*.py'):
    subprocess.check_call(['python', test, os.path.dirname(test)])

for topdir in glob.glob('spacewalk-report-mock/test*'):
    for dirname, dirnames, filenames in os.walk(topdir):
        datafiles.append(('share/splice-testing-tools/' + dirname, map(lambda x: dirname + "/" + x, [fn for fn in filenames if fn.endswith(".csv")])))

setup(name='splicetestlib',
    version='0.1',
    description='Splice Testing library',
    author='Vitaly Kuznetsov',
    author_email='vitty@redhat.com',
    url='https://github.com/RedHatQE/splice-testing-tools',
    license="GPLv3+",
    packages=[
        'splicetestlib'
        ],
    data_files=datafiles,
    classifiers=[
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Operating System :: POSIX',
            'Intended Audience :: Developers',
            'Development Status :: 4 - Beta'
    ],
    scripts=glob.glob('scripts/*')
)
