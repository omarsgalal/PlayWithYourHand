from morphology import calcMorphology
import cv2
import numpy as np
from SkinModel.SkinModel import SkinModel
from morphology import MorphologyDetector
from motionDetection import MotionDetector



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
        return (self.finalOut, self.backgroundSubtraction, self.morphologyWeight, self.getBackgroundModel(), self.getSkinBackgroundModel()),('finalOut', 'backgroundSubtraction','morphologyWeight','backgroundModel','skinBackgroundModel')
    
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
        backgroundSubtraction = (backgroundSubtraction - np.min(backgroundSubtraction))/np.ptp(backgroundSubtraction)

        skinColorDetection = self.__skinModel__.detect(currFrame_rgb)
        morphologyWeight = calcMorphology(backgroundSubtraction)

        # showImages([backgroundSubtraction,self.backgroundModel,skinColorDetection,morphologyWeight], ["bgS","bgm","skinD","morphW"])
        # showImages([backgroundSubtraction,backgroundModel,skinColorDetection,morphologyWeight])

        finalOut = self.__combine__(backgroundSubtraction, skinColorDetection, morphologyWeight, self.getSkinBackgroundModel())

        self.finalOut = finalOut
        self.backgroundSubtraction = backgroundSubtraction
        self.morphologyWeight = morphologyWeight
        return self.getState()
        # cv2.imshow("res", res)


    def __combine__(self, MD, SCD, morphW, sB):
        # print(MD.shape)
        # print(MD.dtype)
        # print(SCD.shape)
        # print(SCD.dtype)
        # print(morphW.shape)
        # print(morphW.dtype)
        # print(sB.shape)
        # print(sB.dtype)
        rate_img = (MD + SCD + morphW - sB) / 3
        print(rate_img.shape,rate_img.dtype)
        # rate_img = 255*(rate_img - np.min(rate_img))/np.ptp(rate_img).astype(np.uint8)
        final_img = cv2.threshold(rate_img.astype(np.uint8),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[0]
        print(final_img.shape, final_img.dtype)
        return final_img #(final_img - np.min(final_img))/np.ptp(final_img)





def main():
    from VideoSequence import VideoSequence as Vs
    from utils import showImages
    vs = Vs().start()
    while(True):
        frames = vs.process()
        handDetector = HandDetector(frames("rgb")[-2])
        images, titles = handDetector.detect(frames('gray'),frames('rgb')[0])
        showImages(images, titles)
        key = cv2.waitKey(10)
        if key == 27 or 0xff:
            break
if __name__ == "__main__":
    main()