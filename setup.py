from distutils.core import setup
from Cython.Build import cythonize

modules = ("core/context.pyx", "core/calc.pyx",
           )


setup(
    ext_modules = cythonize(modules,annotate=True)
)
