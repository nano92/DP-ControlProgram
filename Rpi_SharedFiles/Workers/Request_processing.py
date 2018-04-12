'''
Created on Nov 14, 2016

@author: nanogallet
'''
import subprocess
import os
import time
import signal
import re
import glob
from PIL import Image
from time import sleep

CHILD_ID = []
PISHADERTOY_PATH = '/home/pi/Downloads/newCode/pishadertoy/pishadertoy' 
SHADER_IMAGE = '/home/pi/Downloads/newCode/pishadertoy/shaders/image.f.glsl'
UPLOAD_PATH = '/home/pi/Documents/PixelArtDisplay/ServerFiles/'

def prepareImageCommand(path, queue_display):
    #global current_display
    #application = '/home/pi/Downloads/pishadertoy-master/pishadertoy' 
    print ('from prepare command ' + path)
    absolute_path = UPLOAD_PATH + path
    print('from prepare command ' + absolute_path)
    arguments = ['pishadertoy', SHADER_IMAGE, absolute_path]
    print (arguments)
    #filename = os.path.basename(path)
    #setCurrentlyOnDisplay(filename)
    current_display = os.path.basename(path)
    print(current_display)
    
    addDisplayNameToQueue(current_display, queue_display)

    processCommand(PISHADERTOY_PATH, arguments)

    #give at least 30 seconds to last display
    time.sleep(30)

def prepareGifCommand(path, queue_display): #gfilename (/home/pi/.../mario .gif)
    #imageNameFull = 'mario.gif'
    current_display = os.path.basename(path)
    print(current_display)
    absolute_path = UPLOAD_PATH + path
    
    imageName = absolute_path.replace(".gif","")  
    im = Image.open(absolute_path)
    numberOfFrames = 0;
    
    try:
        while True:
            new_frame = im.convert('RGBA')
            new_frame.save('{0}{1}{2}'.format(imageName,im.tell(),'.png'),'PNG')
            numberOfFrames = im.tell();
            im.seek(im.tell()+1)
    except EOFError:
        pass
    print("done")
    gif_path = "{0}{1}".format(imageName,'.png')
    arguments = ['pishadertoy', SHADER_IMAGE, gif_path, str(numberOfFrames)]

    addDisplayNameToQueue(current_display, queue_display)

    processCommand(PISHADERTOY_PATH, arguments)
    
    #give at least 30 seconds to last display
    time.sleep(30)

def prepareShaderCommand(paths, queue_display):
    matches = re.findall('uploads\/[a-zA-Z\d\.]*',paths, re.IGNORECASE)
    image_path = UPLOAD_PATH + matches[0]
    shader_path = UPLOAD_PATH + matches[1]
    print('shader_path: ' + shader_path + ' image_path: ' + image_path)

    current_display = os.path.basename(image_path) + ' with shader ' + \
                        os.path.basename(shader_path)

    arguments = ['pishadertoy', shader_path, image_path]

    addDisplayNameToQueue(current_display, queue_display)

    processCommand(PISHADERTOY_PATH, arguments)

    #give at least 30 seconds to last display
    time.sleep(30)

def processCommand(app, args):

    pid = os.fork()
    CHILD_ID.append(pid)
    if pid == 0:
        print('child pid: ', os.getpid())
        os.execvp(app, args)

        os._exit(0)
    
    else:
        print('parent pid:', os.getpid())
        # w = os.waitpid(pid, os.WUNTRACED | os.WCONTINUED)
        # while not os.WIFEXITED(w[1]) and not os.WIFSIGNALED(w[1]):
        #   print(pid)
        #   w = os.waitpid(pid, os.WUNTRACED | os.WCONTINUED)
        #   if w[1] == -1:
        #       print("parent fork error")

    
def checkChildProcess():
    if CHILD_ID:
        for process_ID in CHILD_ID:
            w = os.waitpid(process_ID, os.WNOHANG)
            if w[0] == 0:
                return [True, process_ID]
            else:
                return [False, 0]
    else:
        return [False, 0]

def uploadsFolderCleanup(filename):
    base_file_name = filename.replace(".gif", "")
    
    for file in glob.glob(UPLOAD_PATH + base_file_name + '*.png'):
        if os.path.isfile(file):
            os.remove(file)

def killChildProcess(process_ID):
    CHILD_ID.remove(process_ID)
    os.kill(process_ID, signal.SIGKILL)
    return True

def addDisplayNameToQueue(current_display, queue_display):
    if queue_display.empty():
        queue_display.put(current_display)
    else:
        # We need to empty the queue everytime in order to send up to date data 
        # to the website
        temp = queue_display.get()
        queue_display.put(current_display)