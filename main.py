#########################
#
# Planet Simulation Prog3 2018
#
#########################
import sys

from qtpy import QtWidgets

import core.simulation as simu
from gui.qt_gui import qt_ui

body_list = simu.initialize()
app = QtWidgets.QApplication(sys.argv)
simulation_gui = qt_ui(body_list)
simulation_gui.show()
sys.exit(app.exec_())