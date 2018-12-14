import timeit
import numpy as np
import cv2
mROI = [0,100,2,200]
threshold = 10
mask = np.zeros((720,1200,3),dtype=bool)
def costly_func():
    for i in range(10):
        # mask1 = np.zeros_like(mask,dtype='uint8')
        # mask1[mROI[0]:mROI[1], mROI[2]:mROI[3], :] = 1

        mask2 = np.zeros_like(mask,dtype=bool)
        mask2[mROI[0]:mROI[1], mROI[2]:mROI[3], :] = True

        # check1 = 1- mask1
        check2 = np.invert(mask2)

        # mask1[mROI[0]:mROI[1], mROI[2]:mROI[3], :] = 1
        
        # mask1[mROI[0]:mROI[1], mROI[2]:mROI[3], :] = True
        # mask2 = np.invert(mask1)
        # b = np.random.randint(255, size=(720, 1280))
        # binary1 = np.logical_and(a, b)
        # binary2 = cv2.bitwise_and(a, b)
        # binary3 = a* b
        # cv2.threshold(a,127,255,cv2.THRESH_BINARY,dst=b)
    return 

print(timeit.timeit(costly_func, number=100))
# b = np.random.randint(255, size=(720, 1280),dtype='uint8')
# mask1 = np.zeros_like(mask,dtype='uint8')
# mask1[mROI[0]:mROI[1], mROI[2]:mROI[3], :] = 1

# mask2 = np.zeros_like(mask,dtype=bool)
# mask2[mROI[0]:mROI[1], mROI[2]:mROI[3], :] = True

# check1 = 1- mask1
# check2 = np.invert(mask2)
# print(np.array_equal(check1,check2))

# a = np.random.randint(2, size=(720, 1280,3),dtype='uint8')
# b = np.random.randint(2, size=(720, 1280,3),dtype='uint8')

# # cv2.threshold(a,b,1,cv2.THRESH_BINARY)
# c = cv2.bitwise_and(a*255, b)
# c2 = a*b
# print (np.array_equal(c,c2))
# print((cv2.threshold(b,127,1,cv2.THRESH_BINARY)[1]).dtype)
