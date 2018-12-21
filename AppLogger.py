from utils import showImages
from cv2 import imshow,imwrite,bitwise_and
out=False
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

    @classmethod
    def s(cls, image, title, frame = None):
        imwrite('Images/{}.jpg'.format(title), image)
        if type(frame) != type(None):
            imwrite('Images/{}_withImage.jpg'.format(title), bitwise_and(frame,frame,mask=image))
            


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