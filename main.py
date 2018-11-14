#########################
#
# Planet Simulation Prog3 2018
#
#########################
import sys
import core.simulation as s
from PyQt5 import QtWidgets
from gui.qt_gui import qt_ui

if __name__ == '__main__':
    body_list = s.initialize()
    app = QtWidgets.QApplication(sys.argv)
    simulation_gui = qt_ui(body_list)
    simulation_gui.show()
    sys.exit(app.exec_())