import cv2
import numpy as np
from utils import toGray

class VideoSequence:
    def __init__(self):
        pass

    def __readFrame__(self):
        img = self.__cap__.read()[1]
        return cv2.flip(img, 1)
        
    def start(self):
        self.__cap__ = cv2.VideoCapture(0)
        for i in range(10):
            self.__beforePrev__ = self.__readFrame__()

        self.__beforePrev__ = self.__readFrame__()
        self.__beforePrev_g__ = toGray(self.__beforePrev__)
        cv2.waitKey(20)
        self.__prev__ = self.__readFrame__()
        self.__prev_g__ = toGray(self.__prev__)
        cv2.waitKey(20)
        self.__curr__ = self.__readFrame__()
        self.__curr_g__ = toGray(self.__curr__)
        cv2.waitKey(20)

        return self

    def process(self):
        self.__beforePrev__ = self.__prev__
        self.__prev__ = self.__curr__
        self.__curr__ = self.__readFrame__()

        self.__beforePrev_g__ = self.__prev_g__
        self.__prev_g__ = self.__curr_g__
        self.__curr_g__ = toGray(self.__curr__)
        if cv2.waitKey(1) == 27: 
            quit()  # esc to quit

        def getFramesByType(fType):
            return self.getFrames(fType)
        return getFramesByType

    def getFrames(self, fType):
        if (fType.upper() == "BGR"):
            return (self.__curr__, self.__beforePrev__, self.__prev__)
        elif(fType.upper() == "GRAY"):
            return (self.__curr_g__, self.__beforePrev_g__, self.__prev_g__)
        else:
            raise Exception("Not supported frames of type {}, only supproted are 'BGR', 'gray'".format(fType))



if __name__ == "__main__":
    vs = VideoSequence().start()
    while(True):
        frames = vs.process()("BGR")
        cv2.imshow("test diff", cv2.absdiff(frames[-2],frames[0]))