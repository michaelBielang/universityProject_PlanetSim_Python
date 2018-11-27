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
    context = s.initialize(5)
    app = QtWidgets.QApplication(sys.argv)
    simulation_gui = qt_ui(context)
    simulation_gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
