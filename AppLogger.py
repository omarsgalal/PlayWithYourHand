from utils import showImages
from cv2 import imshow

out=True
debug=False
class ImageLogger:
    def __init__(self):
        pass

    @classmethod
    def o(cls, images, titles=None):
        '''
            out images if config 'out' = true, else do nothing
        '''
        if(not out):
            return
        showImages(images, titles) if type(images) == type(()) or type(images) == type([]) else imshow(titles, images)

    @classmethod
    def d(cls, images, titles=None):
        '''
            out images if config 'debug' = true, else do nothing
        '''
        if(not debug):
            return
        showImages(images, titles) if type(images) == type(()) or type(images) == type([]) else imshow(titles, images)        


class GeneralLogger:
    @classmethod
    def o(cls, message, tag=None):
        '''
            out message with tag of specified if config 'out' = true, else do nothing
        '''
        print("[{}]: {}".format(tag, message)) if out else None
        pass

    @classmethod
    def d(cls, message, tag=None):
        '''
            out message with tag of specified if config 'debug' = true, else do nothing
        '''
        print("[{}]: {}".format(tag, message)) if debug else None