'''
Created on Nov 14, 2016

@author: nanogallet
'''
import time
from Workers.Request_processing import prepareImageCommand, checkChildProcess, \
                                        uploadsFolderCleanup, prepareGifCommand,\
                                        killChildProcess, prepareShaderCommand

UPLOAD_PATH = '/home/pi/Documents/PixelArtDisplay/ServerFiles/'

class Server(object):
    '''
    classdocs
    '''
    def __init__(self):
        self.params = []
        self.info_table = {}
    
    def _setInfoTable(self, worker, datapath):
        self.info_table = {worker : datapath}
    
    def _executeTask(self, worker_type, queue_display):
        data_path = self.info_table.get(worker_type)
        
        if worker_type == "i":
            print("image")
            prepareImageCommand(data_path, queue_display)
            #call image processing method
        elif worker_type == "g":
            print("gif")
            prepareGifCommand(data_path, queue_display)
           # test(parameters)
            #shadertoy_command(parameters)
            #call shadertoy request method
        elif worker_type == "s":
            print("shader")
            prepareShaderCommand(data_path, queue_display)
            #call openGL processing method
        else:
            print("Method not found")
            
    def processRequest(self, queue, queue_display):
        data_type = ''
        data_received = ''
        start_time = 0
        while 1:
            if not queue.empty():
                response, process = checkChildProcess()
                if response:
                    killChildProcess(process)
                    if data_type == 'g':
                        uploadsFolderCleanup(data_received)
                    print('Last process terminated, ready to execute')
                    #uploads folder cleanup
                else:
                    print('No process running, ready to execute')

                data = queue.get()
                
                start_time = time.time()
                print('from process request ' + data)
                data_type = data[0]
                data_received = data[:0] + data[1:]

                self._setInfoTable(data_type, data_received)
                self._executeTask(data_type, queue_display)
            else:
                elapsed_time = time.time() - start_time
                response, process = checkChildProcess()
                if response and elapsed_time > 120:
                    killChildProcess(process)
                    if data_type == 'g':
                        uploadsFolderCleanup(data_received)
                    print('Last process terminated, timeout')