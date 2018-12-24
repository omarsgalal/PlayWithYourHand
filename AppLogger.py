from utils import showImages
from cv2 import imshow
import numpy as np
out=False
debug=False
class ImageLogger:
    def __init__(self):
        pass

    @classmethod
    def o(cls, images, titles=None, preFunc = ()):
        '''
            out images if config 'out' = true, else do nothing
        '''
        if(not out):
            return
        images = list(images) if type(images) == type(()) or type(images) == type([]) else [images,]
        if(not titles == None):
            titles = list(titles) if type(titles) == type(()) or type(titles) == type([]) else (titles,)
        for i, _ in enumerate(images):
            for f in preFunc:
                images[i] = f(images[i])
        showImages(images, titles) #if type(images) == type(()) or type(images) == type([]) else imshow(titles, images)

    @classmethod
    def d(cls, images, titles=None, preFunc = ()):
        '''
            out images if config 'debug' = true, else do nothing
        '''
        if(not debug):
            return
        images = list(images) if type(images) == type(()) or type(images) == type([]) else [images,]
        if(not titles == None):
            titles = list(titles) if type(titles) == type(()) or type(titles) == type([]) else (titles,)
        for i, _ in enumerate(images):
            for f in preFunc:
                images[i] = f(images[i])
        showImages(images, titles) #if type(images) == type(()) or type(images) == type([]) else imshow(titles, images)        


class GeneralLogger:
    @classmethod
    def o(cls, message, tag=None):
        '''
            out message with tag of specified if config 'out' = true, else do nothing
        '''
        if(not out):
            return
        print("[{}]: {}".format(tag, message))

    @classmethod
    def d(cls, message, tag=None):
        '''
            out message with tag of specified if config 'debug' = true, else do nothing
        '''
        if(not debug):
            return
        print("[{}]: {}".format(tag, message))