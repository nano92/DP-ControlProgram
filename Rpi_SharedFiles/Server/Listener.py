#!/usr/bin/env python
'''
Created on Nov 15, 2016

@author: nanogallet
'''
import socket
import sys
import os
import stat

def getData(queue, queue_display):

    UDS_address = './uds_socket'
    BUFFER_SIZE = 1024
    
    message_received = ''
    current_display = 'No image on display'
    flag = False
        
    try:
        os.unlink(UDS_address)
    except OSError:
        if os.path.exists(UDS_address):
            raise

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print('UDS_address: ', UDS_address)
    s.bind(UDS_address)
    print('binding')
    s.listen(5)
    
    os.chmod('uds_socket', stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | 
                            stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | 
                            stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH)
  
    while 1:
        print('waiting for a connection')
        conn, addr = s.accept()
        try:   
            print ('Connection address:', str(addr))
                  
            data = conn.recv(BUFFER_SIZE)
            message_received = data
            if(str(message_received, 'utf-8') != 'r'):
                while data:
                    print ('Receiving...')
                    if not data: break
                    data = conn.recv(BUFFER_SIZE)
                    message_received += data
        except socket.error as exc:
            print ("Caught exception socket.error : %s" % exc)
        
        finally:
            print ('Done reciving')
            print (message_received)
            message_received = str(message_received,'utf-8')
            if (message_received == 'r'):
                if not queue_display.empty():
                    current_display = queue_display.get()
                    print("new = " + current_display)
                    conn.send(str.encode(current_display))
                else:
                    print("old = " + current_display)
                    conn.send(str.encode(current_display))
            else:
                queue.put(message_received)

            conn.close()    