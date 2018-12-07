from VideoSequence import VideoSequence as Vs
from HandDetector import HandDetector as Hd
from GestureRecognizer import GestureRecognizer as Gd
from GameController import GameController as Gc
from utils import showImages
from ConfigReader import ConfigReader
import AppLogger as Logger

class AppManager:
    TAG = "AppManager"
    """ this class is the manager of the whole app, define interface between user of the app (developer) and what this app do.
    simply this class manages the communication between 4 main classes (VideoSequence, HandDetector, GestureDetector, GameController)"""
    def __init__(self, output=True,debug=False):
        Logger.debug = debug
        Logger.out = output
        self.vs = Vs().start()
        self.hd = Hd(self.vs.getFrames("BGR")[-2])
        self.gd = Gd()
        self.gc = Gc(ConfigReader.default())


    def showAllImages(self):
        currFrame = self.vs.getFrames("BGR")[0]
        # bgModel = self.hd.getBackgroundModel()
        # skinBgModel = self.hd.getSkinBackgroundModel()
        images, titles = self.hd.getState()
        showImages(images, titles)
        showImages((currFrame,),('Camera',))

    def step(self):
        #* capturing
        frames = self.vs.process()

        #* detection
        self.hd.detect(frames("gray"), frames("BGR")[0])

        #* recognition
        gesture, center = self.gd.recognize(self.hd.roi, self.hd.finalOut)
        Logger.GeneralLogger.o("{} detected in {}".format(gesture, center), tag=self.TAG)

        #* controlling
        self.gc.control(gesture, center)



def main():
    tester = AppManager(output=True, debug=True)
    while(True):
        tester.step()
        #// tester.showAllImages()

if __name__ == "__main__":
    main()