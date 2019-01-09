from multiprocessing import Manager
from multiprocessing.managers import BaseManager, Value
import multiprocessing
from threading import Thread

class TaskManager(BaseManager):
    """
    Subclass of BaseManager with functions to start server for the distribution
    and also manage the client connection.
    """
    pass

    def startup(self,context):
        """
        Initialize necessary information for server and start it
        within a new thread.

        :param context: context object
        """
        master_socket = int(12345)
        self.task_queue = context.InputQueue
        self.result_queue = context.OutputQueue
        manager = Manager()
        self.dict_position = manager.dict()
        self.dict_cycle = manager.dict()
        self.dict_worker_info = manager.dict()

        TaskManager.register('get_job_queue',
                             callable = lambda:self.task_queue)
        TaskManager.register('get_result_queue',
                             callable = lambda:self.result_queue)
        TaskManager.register('get_data',
                             callable = lambda:self.dict_position)
        TaskManager.register('get_cycle',
                             callable = lambda:self.dict_cycle)
        TaskManager.register('set_worker_info',
                             callable = lambda:self.dict_worker_info)
        self.m = TaskManager(address = ('', master_socket),
                        authkey = b'secret')


        thread = Thread(target=self.runServer)
        thread.start()

    def runServer(self):
        print('Starting Server with ID :' + str(self.m.address))
        self.m.get_server().serve_forever()
        self.m.get_server()


    def clientConnect(self,server_ip="localhost"):
        """
        Start connection to server.

        :param server_ip: IP address of the server
        :return: Instanz of Taskmanager
        """
        try:
            server_socket = int(12345)
            m = TaskManager(address=(server_ip, server_socket), authkey = b'secret')
            m.connect()
            return m
        except:
            from gui import qt_gui
            qt_gui.set_status_text("Connection Failed!")
            return None

    def print_worker_info(self,old,new):
        for i in range(old,new):
            print("Execution Worker connected with PID: " + str(self.dict_worker_info.values()[i][1]) + " on Host " + str(self.dict_worker_info.values()[i][0]))
        print("Currently are " + str(new) + "connected to the Master")