from PyQt5 import QtWidgets,uic
import sys,multiprocessing

from gui import opengl_simulation
from gui.galaxy_renderer import galaxy_renderer


class qt_Ui(QtWidgets.QDialog):
    def __init__(self,body_list):
        self.body_list = body_list
        super(qt_Ui, self).__init__()
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

    import core.body as bd
    import numpy as np
    bdy = bd.Body('Test',1,np.array([0.1,0.1,0.1]),100,0.1)
    bdy2 = bd.Body('Test',1,np.array([0.2,0.2,0.2]),100,0.1)

    import numpy as np
    body_list = [bdy,bdy2]
    #Only for Testing without Simulation
    app = QtWidgets.QApplication(sys.argv)
    simulation_gui = qt_Ui(body_list)
    simulation_gui.show()
    sys.exit(app.exec_())
    sys.exit(app.exec_())


