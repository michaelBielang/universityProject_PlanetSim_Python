"""
#################################
#                               #
# Planet Simulation Prog3 2018  #
#                               #
#################################
"""

import sys

from PyQt5 import QtWidgets

from gui.qt_gui import qt_ui


def main():
    """main function"""
    app = QtWidgets.QApplication(sys.argv)
    simulation_gui = qt_ui()
    simulation_gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
