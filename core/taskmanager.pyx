from multiprocessing.managers import BaseManager
from threading import Thread

class TestClass():
    def __init__(self, context):
        self.np_bodies = context.np_bodies
        self.cycle_id = context.cycle_id

    def get_np_bodies(self):
        return self.np_bodies

    def set_np_bodies(self,bodies):
        self.np_bodies = bodies

    def get_cycle_id(self):
        return self.cycle_id

    def set_cycle_id(self,new_cycle_id):
        self.cycle_id = new_cycle_id

class TaskManager(BaseManager):
    pass

    def startup(self,context):

        master_socket = int(12345)
        self.task_queue = context.InputQueue
        self.result_queue = context.OutputQueue
        self.np_bodies = TestClass(context)

        TaskManager.register('get_job_queue',
                             callable = lambda:self.task_queue)
        TaskManager.register('get_result_queue',
                             callable = lambda:self.result_queue)
        TaskManager.register('get_np_bodies',
                             callable = lambda:self.np_bodies)
        TaskManager.register('set_np_bodies',
                             callable = lambda:self.np_bodies)
        self.m = TaskManager(address = ('', master_socket),
                        authkey = b'secret')

        thread = Thread(target=self.runServer)
        thread.start()

    def runServer(self):
        print('starting queue server, socket')
        self.m.get_server().serve_forever()

    def joinQueue(self):
        self.task_queue.join()

    def clientConnect(self,server_ip="localhos7t"):
        server_socket = int(12345)
        TaskManager.register('get_job_queue')
        TaskManager.register('get_result_queue')
        TaskManager.register('get_np_bodies')
        m = TaskManager(address=(server_ip, server_socket), authkey = b'secret')
        m.connect()
        return m
