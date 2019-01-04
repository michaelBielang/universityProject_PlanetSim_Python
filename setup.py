from distutils.core import setup
from Cython.Build import cythonize

modules = ("core/body.pyx", "core/calc.pyx","core/calc.pyx",
           "core/context.pyx","core/simulation.pyx","core/taskmanager.pyx",
           "gui/opengl_simulation.pyx","gui/qt_gui.pyx")


setup(
    ext_modules = cythonize(modules)
)