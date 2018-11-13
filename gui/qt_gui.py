from PyQt5 import QtWidgets,uic
import sys,multiprocessing

from gui import opengl_simulation
from gui.galaxy_renderer import galaxy_renderer


class qt_ui(QtWidgets.QDialog):
    def __init__(self,body_list):
        self.body_list = body_list

        super(qt_ui, self).__init__()
        uic.loadUi('Default_Context_Menu.ui', self)

        self.startButton.clicked.connect(self.start_simulation)
        self.stopButton.clicked.connect(self.stop_simulation)

        #self.SpeedLabel.valuechanged.connect(self.update())
        self.renderer_conn, self.simulation_conn = None, None
        self.render_process = None
        self.simulation_process = None

    def update(self):
        self.SpeedLabel.value = self.SpeedSlider.value
        self.SunMassLabel.value = self.SunMassSlider.value

    def start_simulation(self):
        """
            Start simulation and render process connected with a pipe.
        """
        self.renderer_conn, self.simulation_conn = multiprocessing.Pipe()
        self.simulation_process = \
            multiprocessing.Process(target=opengl_simulation.startup,
                                    args=(self.simulation_conn, self.body_list))
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
    import test.simulation as s

    body_list = s.initialize()
    app = QtWidgets.QApplication(sys.argv)
    simulation_gui = qt_ui(body_list)
    simulation_gui.show()
    sys.exit(app.exec_())


