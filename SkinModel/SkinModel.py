import numpy as np
import cv2
import skimage.io as io
import os 
from skimage.color import rgb2gray,rgb2hsv,hsv2rgb
import sys
sys.path.append('../')
from SkinModel.TrainSkinModel import TrainSkinModel

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

        
    def getModels(self):
        return self.skinHisto, self.nonskinHisto
    
    def detect(self,img,mode='BGR',threshold = 1):

        #trail
        return self.detectNonProbability(img)

        if mode == 'BGR':
            img = cv2.cvtColor(img.astype('uint8'), cv2.COLOR_BGR2HSV)
        elif mode=='RGB':
            img = rgb2hsv(img)
        elif mode=='HSV':
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
        # newImg = newImg * mask
        mask = cv2.medianBlur(mask,3)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        # mask = cv2.medianBlur(mask,3)
        # kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        # mask = cv2.erode(mask, np.ones((2,2),dtype='uint8'), iterations = 1)
        mask = cv2.dilate(mask, kernel, iterations = 3)
        return mask

    def detectNonProbability(self, img):
        mask1 = np.log((img[:, :, 2] / (img[:, :, 1] + 0.00001)) + 0.00001)
        mask2 = np.log((img[:, :, 0] / (img[:, :, 1] + 0.00001)) + 0.00001)

        mask1 = (mask1 > 0.15) * (mask1 < 1.1)
        mask2 = (mask2 > -4) * (mask2 < 0.3)

        mask = (mask1 * mask2 ).astype('uint8')
        return mask

def main():
    from VideoSequence import VideoSequence as Vs
    from utils import showImages
    s = SkinModel()
    vs = Vs().start()
    while(True):
        frames = vs.process()
        img = s.detect(frames("BGR")[-2])
        showImages([img*255], ["skin detector Model only"])
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
if __name__ == "__main__":
    main()