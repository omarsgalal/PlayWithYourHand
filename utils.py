import cv2
import numpy as np

def toGray(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def showImages(images, titles=None):
    n_ims = len(images)
    if titles is None: titles = ['(%d)' % i for i in range(1,n_ims + 1)]
    for image,title in zip(images,titles):
        cv2.imshow(title, image)


def get3DMask(mask2D):
	mask3D = np.empty((mask2D.shape[0], mask2D.shape[1], 3))
	mask3D[:, :, 0] = mask2D
	mask3D[:, :, 1] = mask2D
	mask3D[:, :, 2] = mask2D
	return mask3D