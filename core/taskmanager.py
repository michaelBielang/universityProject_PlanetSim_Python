from multiprocessing.managers import BaseManager
from threading import Thread

class TestClass():
    def __init__(self, bodies):
        self.np_bodies = bodies

    def get_np_bodies(self):
        return self.np_bodies
    def set_new_pos_and_vel(self, id, item):
        self.np_bodies[id][0:3] = item[0:3]
        self.np_bodies[id][3:6] = item[3:6]

class TaskManager(BaseManager):
    pass

    def startup(self,context):

        master_socket = int(12345)
        self.task_queue = context.InputQueue
        self.result_queue = context.OutputQueue
        self.np_bodies = TestClass(context.np_bodies)

        TaskManager.register('get_job_queue',
                             callable = lambda:self.task_queue)
        TaskManager.register('get_result_queue',
                             callable = lambda:self.result_queue)
        TaskManager.register('get_np_bodies',
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

    def clientConnect(self):
        server_ip = "localhost"
        server_socket = int(12345)
        TaskManager.register('get_job_queue')
        TaskManager.register('get_result_queue')
        TaskManager.register('get_np_bodies')
        m = TaskManager(address=(server_ip, server_socket), authkey = b'secret')
        m.connect()
        return m
