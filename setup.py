# to compile all
# $python setup.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

extensions = [Extension("*",["./lib/*.pyx"])]
setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = cythonize(extensions)
)
