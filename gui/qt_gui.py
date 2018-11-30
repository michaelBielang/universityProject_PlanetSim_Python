"""QT_GUI"""

import sys
import core.simulation as s
import multiprocessing
from PyQt5 import QtWidgets, uic

from gui import opengl_simulation
from gui.galaxy_renderer import galaxy_renderer


class qt_ui(QtWidgets.QDialog):
    def __init__(self):

        super(qt_ui, self).__init__()
        import os
        old_working_dir = os.getcwd()
        new_working_dir = os.path.dirname(os.path.abspath(__file__))

        os.chdir(new_working_dir)
        uic.loadUi('Startmenu.ui', self)
        os.chdir(old_working_dir)

        self.startButton.clicked.connect(self.start_random)
        self.sosy.clicked.connect(self.start_sosy)
        self.stopButton.clicked.connect(self.stop_simulation)
        self.objcountslider.valueChanged.connect(self.update)
        self.maxmassslider.valueChanged.connect(self.update)
        self.maxdistslider.valueChanged.connect(self.update)
        self.sunmulslider.valueChanged.connect(self.update)
        # self.SpeedSlider.valueChanged.connect(self.update)
        # self.SunMassSlider.valueChanged.connect(self.update)

        # self.SpeedLabel.valuechanged.connect(self.update())
        self.renderer_conn, self.simulation_conn = None, None
        self.render_process = None
        self.simulation_process = None

    def update(self):
        # self.SpeedLabel.value = self.SpeedSlider.value()
        # self.SunMassLabel.value = self.SpeedSlider.value()
        self.objcountdisp.display(self.objcountslider.value())
        self.maxmassdisp.display(self.maxmassslider.value())
        self.maxdistdisp.display(self.maxdistslider.value())
        self.sunmuldisp.display(self.sunmulslider.value() / 10)

    def start_random(self):
        self.start_simulation(False)

    def start_sosy(self):
        self.start_simulation(True)

    def start_simulation(self, sosy):
        """
            Start simulation and render process connected with a pipe.
        """
        if sosy is True:
            context = s.initialize()
        else:
            context = s.initialize_random(self.objcountslider.value()
                                          , -self.maxdistslider.value() * 10**9
                                          , self.maxdistslider.value() + 10**9
                                          , self.maxmassslider.value() * 10**24)

        context.add_body_mass(0, self.sunmulslider.value() / 10)
        # context.add_speed(self.SpeedSlider.value()/10)

        self.renderer_conn, self.simulation_conn = multiprocessing.Pipe()
        self.simulation_process = \
            multiprocessing.Process(target=opengl_simulation.startup,
                                    args=(self.simulation_conn, context))
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

#
# if __name__ == '__main__':
#    import core.simulation as s
#    body_list = s.initialize()
#    app = QtWidgets.QApplication(sys.argv)
#    simulation_gui = qt_ui(body_list)
#    simulation_gui.show()
#    sys.exit(app.exec_())
