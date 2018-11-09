from PyQt5 import QtCore, QtGui, QtWidgets,uic
import sys,multiprocessing

import gui.galaxy_renderer
from gui.galaxy_renderer import simulation_mockup, galaxy_renderer


class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Default_Context_Menu.ui', self)
        self.startButton.clicked.connect(self.start_simulation)
        self.stopButton.clicked.connect(self.stop_simulation)
        #self.SpeedLabel.valuechanged.connect(self.update())
        self.show()
    def update(self):
        self.SpeedLabel.value = self.SpeedSlider.value
        self.SunMassLabel.value = self.SunMassSlider.value

    def start_simulation(self):
        """
            Start simulation and render process connected with a pipe.
        """
        self.renderer_conn, self.simulation_conn = multiprocessing.Pipe()
        self.simulation_process = \
            multiprocessing.Process(target=simulation_mockup.startup,
                                    args=(self.simulation_conn, 16, 1))
        self.render_process = \
            multiprocessing.Process(target=galaxy_renderer.startup,
                                    args=(self.renderer_conn, 60), )
        self.simulation_process.start()
        self.render_process.start()

    def stop_simulation(self):
        """
            Stop simulation and render process by sending END_MESSAGE
            through the pipes.
        """
        if self.simulation_process is not None:
            from gui.galaxy_renderer.simulation_constants import END_MESSAGE
            self.simulation_conn.send(END_MESSAGE)
            self.simulation_process = None

        if self.render_process is not None:
            self.renderer_conn.send(END_MESSAGE)
            self.render_process = None

    def exit_application(self):
        """
            Stop simulation and exit.
        """
        self.stop_simulation()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    simulation_gui = Ui()
    simulation_gui.show()
    #simulation_gui.start_simulation()
    sys.exit(app.exec_())
    sys.exit(app.exec_())