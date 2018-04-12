import os, time

UPLOADS_PATH = "/home/pi/Documents/PixelArtDisplay/ServerFiles/uploads"

def uploadCleaning():
    fileToDel = []
    checkUploadTime(fileToDel)
    deleteFiles(fileToDel)


def checkUploadTime(fileToDel):
    months = time.strftime('%m', time.gmtime())
    days = time.strftime('%d', time.gmtime())
    for filename in os.listdir(UPLOADS_PATH):
        full_name_path = UPLOADS_PATH + '/' + filename

        infoD = time.strftime('%d',time.gmtime(os.path.getmtime(full_name_path)))
        infoM = time.strftime('%m',time.gmtime(os.path.getmtime(full_name_path)))

        if int(months)*int(days) - int(infoD)*int(infoM) > 30:
            fileToDel.append(full_name_path)

def deleteFiles(fileToDel):
    for file in fileToDel:
        os.remove(file)