import numpy as np
import cv2
import skimage.io as io
import os 
from skimage.color import rgb2gray,rgb2hsv,hsv2rgb
from TrainSkinModel import TrainSkinModel
from scipy import ndimage
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

        self.lower = np.array([5, 5, 80], dtype = "uint8")
        self.upper = np.array([50, 175, 250], dtype = "uint8")

        
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



    def detectRange(self,img,mode='BGR'):
        if mode == 'BGR':
            img = cv2.cvtColor(img.astype('uint8'), cv2.COLOR_BGR2HSV)
        elif mode=='RGB':
            img = rgb2hsv(img)
        elif mode=='HSV':
            pass
        else:
            raise ValueError('Image mode is not RGB nor HSV')

        skinMask = cv2.inRange(img, self.lower, self.upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
        skinMask = cv2.erode(skinMask, kernel, iterations = 2)
        # skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
        # print(np.max(skinMask),np.min(skinMask))
        return (skinMask/255.0).astype('uint8')

    def detectRangeAllSpaces (self,img,mode='BGR'):
        """https://arxiv.org/pdf/1708.02694.pdf"""
        """https://www.researchgate.net/publication/26593885_A_Skin_Detection_Approach_Based_on_Color_Distance_Map"""
        if mode == 'BGR':
            rgb = img[...,::-1]
            hsv = cv2.cvtColor(img.astype('uint8'), cv2.COLOR_BGR2HSV)
        elif mode=='RGB':
            rgb = img
            hsv = rgb2hsv(img)
        elif mode=='HSV':
            rgb = hsv2rgb(img)
            hsv = img
        else:
            raise ValueError('Image mode is not RGB nor HSV')

        lowerHSV = np.array([0, 0, 0], dtype = "uint8")
        upperHSV = np.array([50, 175, 255], dtype = "uint8")

        lowerRGB = np.array([95, 40, 20], dtype = "uint8")
        upperRGB = np.array([255, 255, 255], dtype = "uint8")

        mask1 = cv2.inRange(hsv, lowerHSV, upperHSV)
        mask2 = cv2.inRange(rgb, lowerRGB, upperRGB)
        #  R > G and R > B and | R - G | > 15 and A > 15
        mask3 = (rgb[:,:,0] > rgb[:,:,1]) * (rgb[:,:,0] > rgb[:,:,2]) * ((rgb[:,:,0] - rgb[:,:,1]) > 15)

        skinMask =  mask1 * mask2 * mask3

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
        skinMask = cv2.erode(skinMask, kernel, iterations = 2)
        return skinMask
        




def main():
    s = SkinModel()
    # pskin = s.skinHisto *1.0 / s.Tskin  + 0.00000000001
    # pnon = s.nonskinHisto*1.0 / s.Tnon  + 0.000001
    # # for x in range(100):
    # x = 1
    # mask = np.array(pnon/pskin < x,dtype=np.uint8)
    # obj = ndimage.find_objects(mask)
    # if obj:
    #     print(mask[obj[0]].shape)
    #     print(obj,np.max(mask))


    # resultImageDiff, _ = ndimage.measurements.label(mask)
    # objs = ndimage.find_objects(resultImageDiff)

    # max_area = 0
    # mROI=[0,0,0,0]
    # for obj in objs:
    #     area = (obj[0].start - obj[0].stop ) * (obj[1].start - obj[1].stop) 
    #     if area > max_area:
    #         max_area = area
    #         # mROI = [obj[0].start, obj[0].stop, obj[1].start, obj[1].stop]#ymin,ymax,xmin,xmax
    #         mROI = obj

    # print (mROI)


    vs = cv2.VideoCapture(0)
    i = 0
    while(True):
        # frames = vs.process()
        img = vs.read()[1]
        img = cv2.flip(img, 1)
        # frames = [s.detect(img,x) for x in range(0,1,0.1)]
        # for x in range(10):
        frame = s.detectRangeAllSpaces(img)
        # cv2.imshow("skin frame",frame*255)
        # mask = frame.copy()
        # mask = cv2.erode(mask, np.ones((7,7)), iterations = 5)
        # mask = cv2.dilate(mask, np.ones((7,7)), iterations = 5)
            
        while i<25:
            mask = frame.copy()
            mask = cv2.erode(mask, np.ones((7,7)), iterations = i)
            mask = cv2.dilate(mask, np.ones((7,7)), iterations = i)
            resultImageDiff, _ = ndimage.measurements.label(mask)
            objs = ndimage.find_objects(resultImageDiff)
            if (len(objs) == 1):
                print(i)
                break
            i += 1
        i %= 25

        cv2.imshow("frame",img)
        cv2.imshow("x= {}",cv2.bitwise_and(img,img,mask = mask))
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
            
if __name__ == "__main__":
    main()