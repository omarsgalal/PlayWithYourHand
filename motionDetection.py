import cv2
from scipy import ndimage
from time import sleep
import numpy as np
from scipy.ndimage import (label,find_objects)
from AppLogger import ImageLogger as ILog, GeneralLogger as GLog

class MotionDetector():
    def __init__(self, initialBackground):
        self.backgroundModel = initialBackground
        self.threshold = np.ones_like(self.backgroundModel[:,:,0]) #initial value of threshold used in background subtraction
        self.threshold *= 30


    def ImageDiff (self, beforeLastFrameGray,lastFrameGray,currentFrameGray,threshold=30):
        diff1 = cv2.absdiff(currentFrameGray,lastFrameGray)
        diff2 = cv2.absdiff(currentFrameGray,beforeLastFrameGray)    
        binary1 = diff1 > threshold
        binary2 = diff2 > threshold
        resultImageDiff = binary1 * binary2
        resultImageDiff = cv2.erode(resultImageDiff.astype('uint8'), np.ones((5, 5),dtype='uint8'), iterations = 2)

        ILog.d((resultImageDiff * 255).astype('uint8'), 'imgdiff')

        #resultImageDiff, _ = ndimage.measurements.label(resultImageDiff)
        objs = ndimage.find_objects(resultImageDiff)

        '''max_area = 0
        mROI=[0,0,0,0]
        for obj in objs:
            area = (obj[0].start - obj[0].stop ) * (obj[1].start - obj[1].stop) 
            if area > max_area:
                max_area = area
                mROI = [obj[0].start, obj[0].stop, obj[1].start, obj[1].stop]#ymin,ymax,xmin,xmax

        print (mROI)'''

        if not objs:
            mROI=[0,0,0,0]
        else:        
            # not good Kaseb
            mROI=[objs[0][0].start,objs[0][0].stop,objs[0][1].start,objs[0][1].stop]#ymin,ymax,xmin,xmax
        return resultImageDiff, mROI



    def BackGroundSubtraction(self, currentFrame, mROI, skinBModel, alpha=0.9):
        diffBackgroundSubtraction = np.linalg.norm(cv2.absdiff(self.backgroundModel, currentFrame),axis=2)#,keepdims=True)
        # one cancelled rule for using skin background model while subtracting
        # skinBModel = 2 * skinBModel + 1
        #binaryBackgroundSubtraction = (diffBackgroundSubtraction > self.threshold ).astype('uint8')#  / skinBModel)#.astype(int)

        #trial to fill gaps due to subtraction Samir
        # binaryBackgroundSubtraction = cv2.dilate(binaryBackgroundSubtraction, np.ones((3,3),dtype='uint8'), iterations = 3)
        # binaryBackgroundSubtraction = cv2.erode(binaryBackgroundSubtraction, np.ones((3,3),dtype='uint8'), iterations = 3)        
        

        # mask = cv2.erode(skinBModel, np.ones((7,7)), iterations = 2)
        # mask = cv2.dilate(mask, np.ones((15,15)), iterations = 3)

        mask1 = np.zeros_like(self.backgroundModel).astype(bool)
        mask1[mROI[0]:mROI[1], mROI[2]:mROI[3], :] = True
        mask2 = np.invert(mask1)

        skinBModelT = -1 * skinBModel.astype(float) * mask1[:, :, 0] / 2 + 1
        
        binaryBackgroundSubtraction = (diffBackgroundSubtraction > (self.threshold * skinBModelT) ).astype(float)#  / skinBModel)#.astype(int)
        binaryBackgroundSubtraction = (1 / (2 * skinBModelT)) * binaryBackgroundSubtraction
        

        ILog.d((mask1 * 255).astype('uint8'), 'mroi')
        self.backgroundModel = (mask1 * self.backgroundModel + mask2 * self.backgroundModel * alpha + mask2 * (1 - alpha) * currentFrame).astype('uint8')

        self.threshold = mask1[:,:,0] * self.threshold + mask2[:,:,0] * alpha * self.threshold + 5 * (1 - alpha) * diffBackgroundSubtraction * mask2[:,:,0]

        return binaryBackgroundSubtraction, mask1[:, :, 0]



    def detect(self, frames_gray, currFrame_rgb, skinBModel):
        # why we don't use the Image Diffrence?
        resultImageDiff, mROI = self.ImageDiff(frames_gray[1],frames_gray[2],frames_gray[0])
        resultBackgroundSub, mROI = self.BackGroundSubtraction(currFrame_rgb, mROI, skinBModel)
        return mROI, resultBackgroundSub

    def gitBackgroundModel(self):
        return self.backgroundModel