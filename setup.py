#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

import sys
import os.path

def get_rootdir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
def get_includedir():
    return '.'

def get_swigdir():
    return os.path.join(get_rootdir(), 'swig')

#import os; os.environ['CC'] = 'g++'; os.environ['CXX'] = 'g++';
#os.environ['CPP'] = 'g++'; os.environ['LDSHARED'] = 'g++'

from distutils.core import setup, Extension

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


simstring_module = Extension(
    '_simstring',
    sources = [
        'export.cpp',
        'export_wrap.cpp',
    ],
    include_dirs=[get_includedir()] + additional_include_dirs,
    library_dirs=library_dirs,
    extra_link_args=libs,
    extra_compile_args=extra_compile_args,
    language='c++',
    )

setup(
    name = 'simstring-quickumls',
    version = '1.1.5r1',
    author = 'Naoaki Okazaki & Blink Health & Luca Soldaini',
    author_email = 'luca@ir.cs.georgetown.edu',
    description = "SimString Python module adapted to work with quickumls",
    ext_modules = [simstring_module],
    py_modules = ["simstring"]
)

