import cv2
from scipy import ndimage
from time import sleep
import numpy as np
from scipy.ndimage import (label,find_objects)
from timeit import default_timer

class MotionDetector():
    def __init__(self, initialBackground):
        self.backgroundModel = initialBackground
        self.threshold = np.ones_like(self.backgroundModel[:,:,0]) #initial value of threshold used in background subtraction
        self.threshold *= 30


    def ImageDiff (self, beforeLastFrameGray,lastFrameGray,currentFrameGray,threshold=30):
        diff1 = cv2.absdiff(currentFrameGray,lastFrameGray)
        diff2 = cv2.absdiff(currentFrameGray,beforeLastFrameGray)    
        binary1 = diff1>threshold
        binary2 = diff2>threshold
        resultImageDiff = binary1 * binary2
        objs = ndimage.find_objects(resultImageDiff)
        if not objs:
            mROI=[0,0,0,0]
        else:        
            # not good Kaseb
            mROI=[objs[0][0].start,objs[0][0].stop,objs[0][1].start,objs[0][1].stop]#ymin,ymax,xmin,xmax
        return resultImageDiff, mROI    



    def BackGroundSubtraction(self, currentFrame, mROI, skinBModel):
        diffBackgroundSubtraction = np.linalg.norm(cv2.absdiff(self.backgroundModel, currentFrame),axis=2)#,keepdims=True)
        # one cancelled rule for using skin background model while subtracting
        # skinBModel = 2 * skinBModel + 1
        binaryBackgroundSubtraction = (diffBackgroundSubtraction > self.threshold )#  / skinBModel)#.astype(int)
        # not good Kaseb
        # binaryBackgroundSubtractionGray = cv2.cvtColor(binaryBackgroundSubtraction.astype('uint8'), cv2.COLOR_BGR2GRAY)
        mask1 = np.zeros_like(self.backgroundModel).astype(bool)
        mask1[mROI[0]:mROI[1], mROI[2]:mROI[3], :] = True
        mask2 = np.invert(mask1)
        self.backgroundModel = (mask1 * self.backgroundModel + mask2 * self.backgroundModel * 0.7 + mask2 * 0.3 * currentFrame).astype('uint8')

        self.threshold = mask1[:,:,0] * self.threshold + mask2[:,:,0] * 0.7 * self.threshold + 5 * 0.3 * diffBackgroundSubtraction * mask2[:,:,0]

        return binaryBackgroundSubtraction.astype('uint8')


    def detect(self, frames_gray, currFrame_rgb, skinBModel):
        resultImageDiff, mROI = self.ImageDiff(frames_gray[1],frames_gray[2],frames_gray[0])
        resultBackgroundSub = self.BackGroundSubtraction(currFrame_rgb, mROI, skinBModel)
        return mROI, resultBackgroundSub

    def gitBackgroundModel(self):
        return self.backgroundModel