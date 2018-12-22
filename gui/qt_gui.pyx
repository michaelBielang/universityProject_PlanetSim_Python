"""QT_GUI"""

import multiprocessing
import configparser


from PyQt5 import QtWidgets, uic

import core.context
import core.simulation as s
from gui import opengl_simulation
from gui.galaxy_renderer import galaxy_renderer


class qt_ui(QtWidgets.QDialog):
    def __init__(self):
        """
        Initialise the QT App
        """

        super(qt_ui, self).__init__()
        import os
        old_working_dir = os.getcwd()
        new_working_dir = os.path.dirname(os.path.abspath(__file__))

        os.chdir(new_working_dir)
        uic.loadUi('Startmenu.ui', self)
        os.chdir(old_working_dir)

        #Click Handler
        self.startButton.clicked.connect(self.start_random)
        self.sosy.clicked.connect(self.start_sosy)
        self.stopButton.clicked.connect(self.stop_simulation)
        self.objcountslider.valueChanged.connect(self.update)
        self.minmass.valueChanged.connect(self.update)
        self.maxmass.valueChanged.connect(self.update)
        self.minrad.valueChanged.connect(self.update)
        self.maxrad.valueChanged.connect(self.update)
        self.maxdistslider.valueChanged.connect(self.update)
        self.sunmulslider.valueChanged.connect(self.update)
        self.connectbutton.clicked.connect(self.client_connect)
        self.disconnectbutton.clicked.connect(self.client_disconnect)

        self.disconnectbutton.setEnabled(False)

        #Ip/port aus configfile lesen
        conf = configparser.ConfigParser()
        conf.read("connection_config.ini")
        self.iptext.setText(conf['Connection']['ip'])
        self.porttext.setText(conf['Connection']['port'])

        self.renderer_conn, self.simulation_conn = None, None
        self.render_process = None
        self.simulation_process = None

    def update(self):
        """
        Slider Updates
        :return:
        """
        # self.SpeedLabel.value = self.SpeedSlider.value()
        # self.SunMassLabel.value = self.SpeedSlider.value()
        self.objcountdisp.display(self.objcountslider.value())
        self.maxmassdisp.display(self.maxmassslider.value())
        self.maxdistdisp.display(self.maxdistslider.value())
        self.sunmuldisp.display(self.sunmulslider.value() / 10)

        if self.maxmass.value() < self.minmass.value():
            self.maxmass.setValue(self.minmass.value())
        if self.maxrad.value() < self.minrad.value():
            self.maxrad.setValue(self.minrad.value())

    def start_random(self):
        """
        Start the Randonm
        :return:
        """
        self.start_simulation(False)

    def start_sosy(self):
        """
        Start the Sun System
        :return:
        """
        self.start_simulation(True)

    def client_connect(self):
        context = core.context.context(1)
        context.InitParralelWorkers(self.iptext.text())
        self.connectbutton.setEnabled(False)
        self.diconnectbutton.setEnabled(True)

    def client_disconnect(self):
        context = core.context.context(1)
        context.ExitParralelWorkers()
        self.connectbutton.setEnabled(True)
        self.disconnectbutton.setEnabled(False)

    def start_simulation(self, sosy):
        """
            Start simulation and render process connected with a pipe.
        """
        if sosy is True:
            context = s.initialize()
        else:
            context = s.initialize_random(self.objcountslider.value(),
                                          -self.maxdistslider.value() * 10**9,
                                          self.maxdistslider.value() + 10**9,
                                          self.minrad.value() / 100,
                                          self.maxrad.value() / 100,
                                          self.minmass.value() * 10**24,
                                          self.maxmass.value() * 10**24,)

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
