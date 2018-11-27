"""QT_GUI"""

import sys
import multiprocessing
from PyQt5 import QtWidgets, uic

from gui import opengl_simulation
from gui.galaxy_renderer import galaxy_renderer


class qt_ui(QtWidgets.QDialog):
    def __init__(self, context):
        self.context = context

        super(qt_ui, self).__init__()
        import os
        old_working_dir = os.getcwd()
        new_working_dir = os.path.dirname(os.path.abspath(__file__))

        os.chdir(new_working_dir)
        uic.loadUi('Default_Context_Menu.ui', self)
        os.chdir(old_working_dir)

        self.startButton.clicked.connect(self.start_simulation)
        self.stopButton.clicked.connect(self.stop_simulation)
        self.SpeedSlider.valueChanged.connect(self.update)
        self.SunMassSlider.valueChanged.connect(self.update)

        # self.SpeedLabel.valuechanged.connect(self.update())
        self.renderer_conn, self.simulation_conn = None, None
        self.render_process = None
        self.simulation_process = None

    def update(self):
        # self.SpeedLabel.value = self.SpeedSlider.value()
        # self.SunMassLabel.value = self.SpeedSlider.value()
        self.SpeedLabel.setText(str(self.SpeedSlider.value()/10))
        self.SunMassLabel.setText(str(self.SunMassSlider.value()/10))

    def start_simulation(self):
        """
            Start simulation and render process connected with a pipe.
        """

        self.context.add_body_mass(0, self.SunMassSlider.value()/10)
        #self.context.add_speed(self.SpeedSlider.value()/10)

        self.renderer_conn, self.simulation_conn = multiprocessing.Pipe()
        self.simulation_process = \
            multiprocessing.Process(target=opengl_simulation.startup,
                                    args=(self.simulation_conn, self.context))
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
