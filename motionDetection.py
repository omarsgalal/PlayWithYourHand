import cv2
from time import sleep
import numpy as np
from scipy.ndimage import find_objects
from AppLogger import ImageLogger as ILog, GeneralLogger as GLog
from utils import multiplyImage, toType 
class MotionDetector():
    def __init__(self, initialBackground):
        self.backgroundModel = initialBackground
        self.threshold = np.ones_like(self.backgroundModel[:,:,0]) #initial value of threshold used in background subtraction
        self.threshold *= 30


    def ImageDiff (self, beforeLastFrameGray,lastFrameGray,currentFrameGray,threshold=30):
        diff1 = cv2.absdiff(currentFrameGray,lastFrameGray)
        diff2 = cv2.absdiff(currentFrameGray,beforeLastFrameGray)    
        _, binary1 = cv2.threshold(diff1,threshold,1,cv2.THRESH_BINARY)
        _, binary2 = cv2.threshold(diff2,threshold,1,cv2.THRESH_BINARY)

        resultImageDiff = cv2.bitwise_and(binary1, binary2)
        resultImageDiff = cv2.erode(resultImageDiff, np.ones((5, 5),dtype='uint8'), iterations = 2)

        ILog.d(resultImageDiff, 'imgdiff', preFunc=(multiplyImage(255),))

        objs = find_objects(resultImageDiff)

        if not objs:
            mROI=[0,0,0,0]
        else:        
            mROI=[objs[0][0].start,objs[0][0].stop,objs[0][1].start,objs[0][1].stop]
        return resultImageDiff, mROI



    def BackGroundSubtraction(self, currentFrame, mROI, skinBModel, alpha=0.95):
        diffBackgroundSubtraction = np.linalg.norm(cv2.absdiff(self.backgroundModel, currentFrame),axis=2)

        mask1 = np.zeros(self.backgroundModel.shape,dtype='uint8')
        mask1[mROI[0]:mROI[1], mROI[2]:mROI[3],:] = 1
        mask2 = 1 - mask1

        skinBModelT = -1.0 * skinBModel * mask1[:,:,0] / 2 + 1
        
        binaryBackgroundSubtraction = diffBackgroundSubtraction > (self.threshold * skinBModelT) #  / skinBModel)#.astype(int)
        binaryBackgroundSubtraction = (1 / (2 * skinBModelT)) * binaryBackgroundSubtraction
        

        ILog.d(mask1, 'mroi', preFunc=(multiplyImage(255), toType('uint8')))
        self.backgroundModel = (mask1 * self.backgroundModel + mask2 * self.backgroundModel * alpha + mask2 * (1 - alpha) * currentFrame).astype('uint8')

        self.threshold = mask1[:,:,0] * self.threshold + mask2[:,:,0] * alpha * self.threshold + 5 * (1 - alpha) * diffBackgroundSubtraction * mask2[:,:,0]

        return binaryBackgroundSubtraction, mask1[:, :, 0]



    def detect(self, frames_gray, currFrame_rgb, skinBModel):
        resultImageDiff, mROI = self.ImageDiff(frames_gray[1],frames_gray[2],frames_gray[0])
        resultBackgroundSub, mROI = self.BackGroundSubtraction(currFrame_rgb, mROI, skinBModel)
        return mROI, resultBackgroundSub

    def gitBackgroundModel(self):
        return self.backgroundModel