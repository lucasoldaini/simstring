#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

import sys
import re
import os.path
from distutils.core import setup, Extension
from distutils.command.install_lib import install_lib as _install_lib

# PACKAGES = find_packages()

def get_rootdir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
def get_includedir():
    return '.'

def get_swigdir():
    return os.path.join(get_rootdir(), 'swig')

#import os; os.environ['CC'] = 'g++'; os.environ['CXX'] = 'g++';
#os.environ['CPP'] = 'g++'; os.environ['LDSHARED'] = 'g++'

def batch_rename(src, dst, src_dir_fd=None, dst_dir_fd=None):
    '''Same as os.rename, but returns the renaming result.'''
    os.rename(src, dst,
              src_dir_fd=src_dir_fd,
              dst_dir_fd=dst_dir_fd)
    return dst

class _CommandInstallCythonized(_install_lib):
    def __init__(self, *args, **kwargs):
        _install_lib.__init__(self, *args, **kwargs)

    def install(self):
        # let the distutils' install_lib do the hard work
        outfiles = _install_lib.install(self)
        # batch rename the outfiles:
        # for each file, match string between
        # second last and last dot and trim it
        matcher = re.compile('\.([^.]+)\.so$')
        return [batch_rename(file, re.sub(matcher, '.so', file))
                for file in outfiles]

additional_include_dirs = []
library_dirs = None
extra_compile_args = None
libs = []
if sys.platform.startswith("darwin") or sys.platform.startswith("cygwin"):
    libs = ['-liconv']
elif 'conda' in sys.version.lower() and sys.platform.startswith("win"):
    # The conda/Windows-specific setup below assumes that the current conda environment has run something like this :
    # conda install -c conda-forge libiconv
    print('Setting up assuming Anaconda was used to install iconv (conda install -c conda-forge libiconv)')
    python_executable_dir = os.path.dirname(sys.executable)
    anaconda_include_dir = os.path.join(python_executable_dir, 'Library/include')
    anaconda_lib_dir = os.path.join(python_executable_dir, 'Library/lib')
    use_conda_deps = True

    # let's check if these pieces are actually here before we try to give the include/lib hints below
    if not os.path.isfile(os.path.join(anaconda_include_dir, 'iconv.h')):
        print('Could not find header iconv.h at [{0}] so bypassing setup hints.  Verify that iconv was installed with conda.'.format(anaconda_include_dir))
        use_conda_deps = False
    elif not os.path.isfile(os.path.join(anaconda_lib_dir, 'iconv.lib')):
        print('Could not find library iconv.lib at [{0}] so bypassing setup hints. Verify that iconv was installed with conda.'.format(anaconda_lib_dir))
        use_conda_deps = False

    if use_conda_deps:
        libs = ['iconv.lib']
        additional_include_dirs = [anaconda_include_dir]
        library_dirs = [anaconda_lib_dir]
        # The = at the end of this with nothing after causes the symbol to have no associated value (instead of 'const')
        # so that this will compile under MSVC more info here:
        # https://docs.microsoft.com/en-us/cpp/build/reference/d-preprocessor-definitions?view=vs-2017
        extra_compile_args = ['/DICONV_CONST=']
        print('Assuming Python executable [{0}], additional include dir [{1}], additional lib dir [{2}]'.format(python_executable_dir, anaconda_include_dir, anaconda_lib_dir))
        print('Setting extra_compile_args to {0}'.format(extra_compile_args))

        print('NOTE: If there is a failure that rc.exe cannot be found, add the appropriate "WindowsKits" directory to the PATH for either x86 or x64.')
else:
    # need iconv too but without proper -L adding -liconv here won't always work
    libs = []

if sys.platform.startswith("darwin"):
    # On recent macos versions (mojave) it is necessary to specify that libc++ is used instead of libstdc++.
    # Furthermore, '-Wl,-undefined,dynamic_lookup' is necessary to link the right libraries.
    libs += ["-stdlib=libc++", '-Wl,-undefined,dynamic_lookup']
    extra_compile_args = ["-stdlib=libc++"]

with open('README.md') as reader:
        readme = reader.read()

simstring_module = Extension(
    'quickumls_simstring/_simstring',
    sources = [
        'quickumls_simstring/export.cpp',
        'quickumls_simstring/export_wrap.cpp',
    ],
    include_dirs=[get_includedir()] + additional_include_dirs,
    library_dirs=library_dirs,
    extra_link_args=libs,
    extra_compile_args=extra_compile_args,
    language='c++',
    )

setup(
    name = 'quickumls_simstring',
    url = 'https://github.com/Georgetown-IR-Lab/simstring',
    version = '1.1.5r1',
    description=(
        'Clone of simstring designed to work with QuickUMLS. ' 
        'Original version here: http://chokkan.org/software/simstring/'
    ),
    long_description=readme,
    packages=['quickumls_simstring'],
    author = 'Naoaki Okazaki & Blink Health & Luca Soldaini',
    author_email = 'luca@ir.cs.georgetown.edu',
    ext_modules = [simstring_module],
    cmdclass={
        'install_lib': _CommandInstallCythonized,
    },
)

