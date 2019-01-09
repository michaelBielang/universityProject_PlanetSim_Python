import cython
from multiprocessing import Manager
from multiprocessing.managers import BaseManager, Value
import multiprocessing
from threading import Thread

class TaskManager(BaseManager):
    pass

    @cython.initializedcheck(False)
    @cython.overflowcheck(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.nonecheck(False)
    @cython.cdivision(True)
    def startup(self,context):

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

    @cython.initializedcheck(False)
    @cython.overflowcheck(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.nonecheck(False)
    @cython.cdivision(True)
    def runServer(self):
        print('Starting Server with ID :' + str(self.m.address))
        self.m.get_server().serve_forever()


    def clientConnect(self,server_ip="localhost"):
        try:
            server_socket = int(12345)
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