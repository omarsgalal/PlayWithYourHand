from VideoSequence import VideoSequence as Vs
from HandDetector import HandDetector as Hd
from GestureRecognizer import GestureRecognizer as Gd
from GameController import GameController as Gc
from AsyncControlRepeater import AsyncControlRepeater 
from utils import showImages, timeMessage
from ConfigReader import ConfigReader
import AppLogger as Logger
from cv2 import getTickCount, getTickFrequency
class AppManager:
    """ this class is the manager of the whole app, define interface between user of the app (developer) and what this app do.
    simply this class manages the communication between 4 main classes (VideoSequence, HandDetector, GestureDetector, GameController)"""
    TAG = "AppManager"
    def __init__(self, output=True,debug=False):
        Logger.debug = debug
        Logger.out = output
        self.vs = Vs().start()
        self.hd = Hd(self.vs.getFrames("BGR")[-2])
        self.gd = Gd()
        #self.gc = AsyncControlRepeater(Gc(ConfigReader.default()), maxBufferSize=1).start()
        self.gc = Gc(ConfigReader.default())

    def showAllImages(self):
        currFrame = self.vs.getFrames("BGR")[0]
        # bgModel = self.hd.getBackgroundModel()
        # skinBgModel = self.hd.getSkinBackgroundModel()
        images, titles = self.hd.getState()
        showImages(images, titles)
        showImages((currFrame,),('Camera',))

    def step(self):
        startT = getTickCount()
        #* capturing
        e1 = getTickCount()
        frames = self.vs.process()
        Logger.GeneralLogger.o(timeMessage("frame process", e1), tag="TIME")

        #* detection
        e1 = getTickCount()
        self.hd.detect(frames("gray"), frames("BGR")[0])
        Logger.GeneralLogger.o(timeMessage("hand detection", e1), tag="TIME")

        #* recognition
        e1 = getTickCount()
        gesture, center = self.gd.recognize(self.hd.roi, self.hd.finalOut)
        Logger.GeneralLogger.o("{} detected in {}".format(gesture, center), tag=self.TAG)
        Logger.GeneralLogger.o(timeMessage("gesture recognition", e1), tag="TIME")
        endT = getTickCount()
        #* controlling
        #// e1 = getTickCount()
        self.gc.control(gesture, center, (endT - startT) / getTickFrequency())
        #self.gc.addGstRecognition(gesture, center)
        #// Logger.GeneralLogger.o(timeMessage("controlling", e1), tag="TIME")
        Logger.ImageLogger.o(self.vs.getFrames("BGR")[0], 'camera')



def main():
    tester = AppManager(output=True, debug=True)
    while(True):
        tester.step()
        #// tester.showAllImages()
    tester.gc.stop()

if __name__ == "__main__":
    main()