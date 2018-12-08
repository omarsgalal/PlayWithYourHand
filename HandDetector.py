from morphology import calcMorphology
import cv2
import numpy as np
from SkinModel.SkinModel import SkinModel
from morphology import MorphologyDetector
from motionDetection import MotionDetector
from utils import get3DMask
from scipy import ndimage
from AppLogger import ImageLogger as ILog, GeneralLogger as GLog

class HandDetector:
    TAG = "HandDetector"
    # models = TrainSkinModel().loadModel()
    def __init__(self, initialBackground):
        self.backgroundModel = initialBackground
        self.__skinModel__ = SkinModel()
        self.__morphologyWeight = MorphologyDetector()
        self.__motionDetection__ = MotionDetector(initialBackground)
        self.__skinBackgroundModel__ = None
        self.handCout = 0 

    def getState(self):
        return (self.finalOut, (self.backgroundSubtraction * 255).astype('uint8'), self.morphologyWeight, self.getBackgroundModel(), self.getSkinBackgroundModel()*255,self.skinColorDetection*255),('finalOut', 'backgroundSubtraction','morphologyWeight','backgroundModel','skinBackgroundModel','skinFrameModel')
    
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
        
        # should be global not here KASEB
        #backgroundSubtraction = cv2.medianBlur(backgroundSubtraction,3)

        # backgroundSubtraction_mask = get3DMask(backgroundSubtraction)
        # backgroundSubtraction_rgb = backgroundSubtraction_mask * currFrame_rgb

        #multiply by background or not (important)
        skinColorDetection = self.__skinModel__.detect(currFrame_rgb) #* backgroundSubtraction

        #Omar Trial
        skinBackgroundModel = self.getSkinBackgroundModel()
        #backgroundSubtraction += roi * skinBackgroundModel

        morphologyWeight = calcMorphology(backgroundSubtraction)
        handOnly = self.handWithoutFace(currFrame_rgb)

        finalOut = self.__combine__(backgroundSubtraction, skinColorDetection, morphologyWeight, skinBackgroundModel,handOnly)

        self.roi = roi
        self.finalOut = finalOut
        self.backgroundSubtraction = backgroundSubtraction
        self.morphologyWeight = morphologyWeight
        self.skinColorDetection = skinColorDetection
        images, titles = self.getState()
        ILog.d(images, titles)
        return images, titles

    def handWithoutFace(self,img):
        frame = self.__skinModel__.detectRangeAllSpaces(img)
        ILog.d(frame*255, "handWithoutFaceFrame")
        while self.handCout<25:
            mask = frame.copy()
            mask = cv2.erode(mask, np.ones((7,7)), iterations = self.handCout)
            mask = cv2.dilate(mask, np.ones((7,7)), iterations = self.handCout)
            resultImageDiff, _ = ndimage.measurements.label(mask)
            objs = ndimage.find_objects(resultImageDiff)
            if (len(objs) == 1):
                GLog.d(self.handCout, tag=self.TAG)
                break
            self.handCout += 1
        ILog.d(mask*255, "handWithoutFace")
        if self.handCout >= 25:
            self.handCout = 15

        return mask


    def __combine__(self, MD, SCD, morphW, sB,Hand):

        #omar trial
        return self.__combine2__(MD, SCD, sB,Hand)

        rate_img = (np.maximum((MD + SCD + morphW - sB), 0.0) / 3 * 255).astype(np.uint8)
        # rate_img = (MD + morphW).astype(np.uint8)
        _ , final_img = cv2.threshold(rate_img,0, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return final_img

    #omar trial
    def __combine2__(self, MD, SCD, sB,Hand):
        skinDifference = np.maximum(SCD.astype(float) + Hand - cv2.dilate(sB, np.ones((7,7),dtype='float'), iterations = 3), 0)
        #skinDifference = cv2.dilate(skinDifference, np.ones((3, 3)), iterations = 1)
        ILog.d(skinDifference, 'skindiff')
        # skinDifference (From 2 to 0) + 0.9 * MD(From 1 to 0) supposed to devide by (2.9) then * 255 KASEB
        totalDifference = np.minimum((skinDifference + 0.9 * MD) * 255, 255).astype('uint8')
        ILog.d(totalDifference, 'before otsu')
        _ , final_img = cv2.threshold(totalDifference,0, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        final_img = cv2.erode(final_img, np.ones((2, 2)), iterations = 1)
        final_img = cv2.medianBlur(final_img, 5)
        return final_img



            
if __name__ == "__main__":
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
