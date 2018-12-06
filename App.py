from VideoSequence import VideoSequence as Vs
from HandDetector import HandDetector as Hd
from GestureRecognizer import GestureRecognizer as Gd
from GameController import GameController as Gc
from utils import showImages
from ConfigReader import ConfigReader

class AppManager:
    """ this class is the manager of the whole app, define interface between user of the app (developer) and what this app do.
    simply this class manages the communication between 4 main classes (VideoSequence, HandDetector, GestureDetector, GameController)"""
    def __init__(self):
        self.vs = Vs().start()
        self.hd = Hd(self.vs.getFrames("BGR")[-2])
        self.gd = Gd()
        self.gc = Gc(ConfigReader.default())
        pass


    def showAllImages(self):
        currFrame = self.vs.getFrames("BGR")[0]
        # bgModel = self.hd.getBackgroundModel()
        # skinBgModel = self.hd.getSkinBackgroundModel()
        images, titles = self.hd.getState()
        showImages(images, titles)
        showImages((currFrame,),('Camera',))
        pass

    def step(self):
        frames = self.vs.process()
        self.hd.detect(frames("gray"), frames("BGR")[0])
        # should call here GestureDetector then GameController
        gesture, center = self.gd.recognize(self.hd.roi,self.hd.finalOut)
        print(gesture, center)
        self.gc.control(gesture, center)


def main():
    tester = AppManager()
    while(True):
        tester.step()
        tester.showAllImages()

if __name__ == "__main__":
    main()