from PIL import Image
from time import sleep
#import subprocess
#import sys, getopt
import atexit

def processGifCommand(path, queue_display): #gfilename (/home/pi/.../mario .gif)
    #imageNameFull = 'mario.gif'
    imageName = filename.replace(".gif","")

    #try:
    #  opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    #except getopt.GetoptError:
    #   print 'test.py -i <inputfile> -o <outputfile>'
    #   sys.exit(2)
    # for opt, arg in opts:
    #     if opt == '-h':
    #         print 'test.py -i <inputfile> -o <outputfile>'
    #         sys.exit()
    #     elif opt in ("-i", "--ifile"):
    #         imageNameFull = arg

    # imageName = imageNameFull.replace(".gif","")
    
    im = Image.open(filename)

    #commandArray = []

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

    return [imageName, numberOfFrames]

# def fucntionA():
#     command = ["sudo","/home/pi/Downloads/newCode/pishadertoy/pishadertoy", "/home/pi/Downloads/newCode/pishadertoy/shaders/image.f.glsl", "/home/pi/Downloads/newCode/pishadertoy/textures/{0}{1}".format(imageName,'.png'), str(numberOfFrames)]
#     p = subprocess.Popen(command)
#     sleep(30)
#     p.terminate()

    
#if __name__ == "__main__":
#   main(sys.argv[1:])
