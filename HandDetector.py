from morphology import calcMorphology
import cv2
import numpy as np
from SkinModel.SkinModel import SkinModel
from morphology import MorphologyDetector
from motionDetection import MotionDetector
from utils import get3DMask



class HandDetector:
    # models = TrainSkinModel().loadModel()
    def __init__(self, initialBackground):
        self.backgroundModel = initialBackground
        self.__skinModel__ = SkinModel()
        self.__morphologyWeight = MorphologyDetector()
        self.__motionDetection__ = MotionDetector(initialBackground)
        self.__skinBackgroundModel__ = None
        
        pass

    def getState(self):
        return (self.finalOut, self.backgroundSubtraction * 255, self.morphologyWeight, self.getBackgroundModel(), self.getSkinBackgroundModel()*255),('finalOut', 'backgroundSubtraction','morphologyWeight','backgroundModel','skinBackgroundModel')
    
    def updateSkinBackgroundModel(self):
        backgroundModel = self.getBackgroundModel()
        self.__skinBackgroundModel__ = self.__skinModel__.detect(backgroundModel)

    def getSkinBackgroundModel(self):
        return self.__skinBackgroundModel__

    def getBackgroundModel(self):
        return self.__motionDetection__.backgroundModel

    def detect(self, frames_gray, currFrame_rgb):
        self.updateSkinBackgroundModel() # optimize

        roi, backgroundSubtraction = self.__motionDetection__.detect(frames_gray, currFrame_rgb, self.getSkinBackgroundModel())
        #backgroundSubtraction = (backgroundSubtraction - np.min(backgroundSubtraction))/np.ptp(backgroundSubtraction)
        
        # should be global not here
        backgroundSubtraction = cv2.medianBlur(backgroundSubtraction,3)

        backgroundSubtraction_mask = get3DMask(backgroundSubtraction)
        backgroundSubtraction_rgb = backgroundSubtraction_mask * currFrame_rgb
        
       
        # cv2.imshow("our background sub",backgroundSubtraction_rgb.astype('uint8'))

        skinColorDetection = self.__skinModel__.detect(backgroundSubtraction_rgb)
        morphologyWeight = calcMorphology(backgroundSubtraction)

        # showImages([backgroundSubtraction,self.backgroundModel,skinColorDetection,morphologyWeight], ["bgS","bgm","skinD","morphW"])
        # showImages([backgroundSubtraction,backgroundModel,skinColorDetection,morphologyWeight])
        cv2.imshow("skin frame",skinColorDetection*255)
        finalOut = self.__combine__(backgroundSubtraction, skinColorDetection, morphologyWeight, self.getSkinBackgroundModel())

        self.finalOut = finalOut
        self.backgroundSubtraction = backgroundSubtraction
        self.morphologyWeight = morphologyWeight
        return self.getState()
        # cv2.imshow("res", res)


    def __combine__(self, MD, SCD, morphW, sB):
        rate_img = ((MD + SCD + morphW - sB) / 3 * 255).astype(np.uint8)
        ret, final_img = cv2.threshold(rate_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return final_img





def main():
    from VideoSequence import VideoSequence as Vs
    from utils import showImages
    vs = Vs().start()
    while(True):
        frames = vs.process()
        handDetector = HandDetector(frames("BGR")[-2])
        images, titles = handDetector.detect(frames('gray'),frames('BGR')[0])
        showImages(images, titles)
        key = cv2.waitKey(10)
        if key == 27 or 0xff:
            break
if __name__ == "__main__":
    main()