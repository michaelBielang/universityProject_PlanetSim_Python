## Modules needed for Simulation
You need to Install Qt5 in Version 5.x including the QtWidgeds Option
Example for PIP 
> pip install qt5

If you want to modify the qt Desing load the qt4 tools, but you can also do it manually
> pip install qt4-tools

(qt5-tools not avabile via pip)

## Simulation Concept
body_list (of body Class) -> qt_gui -> opengl_simulation -> np.array -> galaxy_render