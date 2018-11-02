import numpy as np
import cv2
import skimage.io as io
import os 
from skimage.color import rgb2gray,rgb2hsv,hsv2rgb

import TrainSkinModel

# skinHisto = np.zeros((256,256,256))
# nonskinHisto = np.zeros((256,256,256))

class SkinModel():
    def __init__(self):
        self.trained = TrainSkinModel()
        self.skinHisto,self.nonskinHisto = self.trained.loadModel()

        self.Tskin = np.sum(self.skinHisto)
        self.Tnon = np.sum(self.nonskinHisto)
        
        self.skinHistoSum = np.sum(self.skinHisto,axis=2)
        self.nonskinHistoSum = np.sum(self.nonskinHisto,axis=2)

        

    def detect(self,img,mode='hsv',threshold = 10):
        if mode='rgb':
            img = rgb2hsv(img)
        elif mode='hsv':
            pass
        else:
            raise ValueError('Image mode is not RGB nor HSV')
            
        # newImg = hsv2rgb(img.copy())
        

        flattedImg = np.reshape(img,(-1, 3)).astype(int)

        pskin = self.skinHisto[list(flattedImg.T)].reshape(img.shape[:-1]) *1.0 / self.Tskin  + 0.00000000001
        pnon = self.nonskinHisto[list(flattedImg.T)].reshape(img.shape[:-1]) *1.0 / self.Tnon  + 0.000001

        # pskin = self.skinHistoSum[list(flattedImg[:,:2].T)].reshape(img.shape[:-1]) *1.0 / self.Tskin  + 0.00000000001
        # pnon = self.nonskinHistoSum[list(flattedImg[:,:2].T)].reshape(img.shape[:-1]) *1.0 / self.Tnon  + 0.000001


        mask = np.array(pnon/pskin < threshold,dtype=np.uint8)

        # newImg = (img.transpose(2,0,1) * mask).transpose(1,2,0)
        #     newImg = newImg * mask

        #     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        #     mask = cv2.medianBlur(mask,3)
        #     mask = cv2.erode(mask, kernel, iterations = 1)
        #     mask = cv2.dilate(mask, kernel, iterations = 3)
        #     mask = cv2.GaussianBlur(mask, (3, 3), 0)
        # skin = cv2.bitwise_and(newImg, newImg, mask = mask)

        return mask
