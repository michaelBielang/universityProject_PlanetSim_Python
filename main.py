"""
#########################
#
# Planet Simulation Prog3 2018
#
#########################
"""

import sys
from PyQt5 import QtWidgets
import core.simulation as s
from gui.qt_gui import qt_ui


def main():
    """main function"""
    body_list = s.initialize()
    app = QtWidgets.QApplication(sys.argv)
    simulation_gui = qt_ui(body_list)
    simulation_gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
