'''
Created on Nov 14, 2016

@author: nanogallet
'''
import threading
import queue as Queue

from Server.Server import Server
from Server.Listener import getData
    
if __name__ == '__main__':
    server = Server()
    N = 100
    queue = Queue.Queue(N)
    queue_display = Queue.Queue(1)
    threads = []

    threads.append(threading.Thread(target= getData, args=[queue, queue_display]))
    threads.append(threading.Thread(target= server.processRequest, \
    								args=[queue, queue_display]))

    for thread in threads:
    	thread.start()
    for thread in threads:
    	thread.join()