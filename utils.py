import cv2


def toGray(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def showImages(images, titles=None):
    n_ims = len(images)
    if titles is None: titles = ['(%d)' % i for i in range(1,n_ims + 1)]
    for image,title in zip(images,titles):
        cv2.imshow(title, image)