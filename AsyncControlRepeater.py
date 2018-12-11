import GameController as gc
from threading import Thread
from Gestures import NO_GST
from AppLogger import GeneralLogger as GLog
class AsyncControlRepeater:
    '''
        A Wrapper class for gameController like object, to make it async and repeat last detection if there is no controlling available
        If the controller is very fast than ratio of sending, this will result to like we have asyc controlling
        If the controller is slower than the ratio of sending, sent gestures will be buffered as max 'AsyncControlRepeater.BUFFER_SIZE'
    '''
    TAG = "AsyncControlRepeater"
    def __init__(self, gameController, maxBufferSize = 600):
        self.gc = gameController
        self.stopped = True
        self.gestures = [(NO_GST, (0,0)), (NO_GST, (0,0)), (NO_GST, (0,0))] #?[revise] always take first three shots as no gst
        self.last = self.gestures[0]
        self.MAX_BUFFER_SIZE = maxBufferSize
        pass


    def addGstRecognition(self, newGstRecognition):
        '''
            Add new gesture recognition to the buffer of game controller
            newGstRecognition: is a tuple of gst and center
        '''
        if(len(self.gestures) >= self.MAX_BUFFER_SIZE):
            return False
        self.gestures.insert(0, newGstRecognition)
        return True

    def start(self, initGst = NO_GST):
        # start the thread (no more)
        # todo, add check for not to create a new thread if it started already
        self.stopped = False
        Thread(target=self.control, args=()).start()
        return self

    def control(self):
        GLog.d("control started", tag = self.TAG)
        while not self.stopped:
            if(len(self.gestures) == 0):
                gesture, center = self.last
                GLog.d("len is 0", tag = self.TAG)        
            else:
                gesture, center = self.gestures.pop()   
                self.last = gesture, center
                GLog.d("handling", tag = self.TAG)        
            self.gc.control(gesture, center)
        GLog.d("control end", tag = self.TAG)
        

    def stop(self):
        self.stopped = True

    