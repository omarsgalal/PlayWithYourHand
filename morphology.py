'''
    There is where I try some python using skimage to test code, algorithm, or to implement new required functionality
'''
import numpy as np
import cv2
from skimage.io import imread
from skimage.morphology import watershed
from scipy import ndimage as ndi
from timeit import default_timer
from time import sleep


def imageDifferencing(pre, curr):
    return cv2.absdiff(curr, pre)

def simulateMorphologyShape():
    sampleImage = imread("sample detected hand.jpg",as_grey=True)
    while(1):
        print('call')
        start = default_timer()
        calcMorphology(sampleImage)
        end = default_timer()
        print('return after', end - start, 'seconds')

def calcMorphology(sampleImage):
    distance = ndi.distance_transform_edt(sampleImage)
    normalizedDistance = (distance - np.min(distance))/np.ptp(distance)
    cv2.waitKey(30)
    return normalizedDistance


class MorphologyDetector:
    def __init__(self):
        pass

    def calculateWeights(self, hand_binary):
        distance = ndi.distance_transform_edt(hand_binary)
        normalizedDistance = (distance - np.min(distance))/np.ptp(distance)
        return normalizedDistance

if __name__ == '__main__':
    simulateMorphologyShape()