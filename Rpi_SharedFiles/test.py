
from Workers.Request_processing import prepareGifCommand, checkChildProcess, uploadsFolderCleanup

def test():
	prepareGifCommand("uploads/fire.gif")
	checkChildProcess()
	uploadsFolderCleanup("uploads/fire.gif")
	
if __name__ == "__main__":
	test()