SimString Python Package
========================

Orginal version by `chokkan`_, available `here`_. New version (compiles
under macOS) from
`here <https://github.com/blinkhealth/simstring-python-package>`__.

Windows/Anaconda/VisualStudio specific steps:

1. Make sure that iconv is available to your desired conda environment:
   ``conda install -c conda-forge libiconv``
2. Then, open a Visual Studio Developer Prompt (e.g. “VS 2015 x64
   Developer Command Prompt” or “VS 2015 x86 Developer Command Prompt”)
3. Now you can any of these commands to build or install:

.. code:: bash

   python setup.py build
   python setup.py install

4. **NOTE**: If there is a failure that ‘rc.exe’ cannot be found, add
   the appropriate WindowKits binary path to PATH. More info on this
   `here <https://stackoverflow.com/questions/14372706/visual-studio-cant-build-due-to-rc-exe>`__.

.. _chokkan: 
.. _here: https://github.com/chokkan/simstring