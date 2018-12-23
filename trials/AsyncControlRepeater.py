import GameController as gc
from threading import Thread
import threading
from queue import Queue
from Gestures import NO_GST
from AppLogger import GeneralLogger as GLog
from cv2 import getTickCount, getTickFrequency
class AsyncControlRepeater:
    '''
        A Wrapper class for gameController like object, to make it async and repeat last detection if there is no controlling available
        If the controller is very fast than ratio of sending, this will result to like we have asyc controlling
        If the controller is slower than the ratio of sending, sent gestures will be buffered as max 'AsyncControlRepeater.BUFFER_SIZE'
    '''
    TAG = "AsyncControlRepeater"
    def __init__(self, gameController, maxBufferSize = 3):
        self.gc = gameController
        self.stopped = True
        self.gestures = [{'GST': NO_GST, 'POS': (0,0), 'duration': 0.0}] #?[revise] always take first three shots as no gst
        self.last = self.gestures[0]
        self.MAX_BUFFER_SIZE = maxBufferSize
        self.prevTick = getTickCount()


    def addGstRecognition(self, gst, center):
        '''
            Add new gesture recognition to the buffer of game controller
            newGstRecognition: is a tuple of gst and center
        '''
        currTick = getTickCount()
        timeElapsed = (currTick - self.prevTick) / getTickFrequency()
        GLog.d(timeElapsed, tag='addGstRecognition: time elapsed')
        self.prevTick = currTick
        if(len(self.gestures) >= self.MAX_BUFFER_SIZE):
            return False
        inserted = {'GST': gst, 'POS': center, 'duration': timeElapsed}
        self.gestures.insert(0, inserted)
        return True

    def start(self, initGst = NO_GST):
        # start the thread (no more)
        self.stopped = False
        Thread(target=self.control, args=()).start()
        return self

    def control(self):
        q = Queue()
        q.get(block=True, timeout=0.01)
        GLog.d("control started", tag = self.TAG)
        while not self.stopped:
            if(False and len(self.gestures) == 1):
                gesture1, center1 = self.last
                gesture2, center2 = self.gestures[-1]
                center = []
                if(gesture1 == gesture2):
                    #TODO c1 is always last center sent
                    #TODO c2 is constant, it is last value in the queue -> we here want to send the value that always evaluate to be
                    #TODO dx at the end same as in first time c2 - c1
                    #TODO To achieve it -> always set last as prev value sent to gc
                    #TODO so what we have now is c2 and lastVale (c1 in scd time)
                    #TODO we need to get what we will send to achieve this equation '? - lastValue = c2 - c1'
                    # for now only know the dir and send a small shift
                    smallShiftingX = 1 if center2[0] - center1[0] > 0 else -1
                    smallShiftingY = 1 if center2[1] - center1[1] > 0 else -1
                    center = center1[0] + smallShiftingX, center1[1] + smallShiftingY   #\? - c1 
                GLog.d("len is 1", tag = self.TAG)        
                self.gc.control(gesture1, center)
                self.last = gesture1, center

            if(len(self.gestures) == 0):
                #todo: make it blocks instead of busy waiting --> Thread.join()
                continue
            else:
                current = self.gestures.pop()
                self.last = current
                GLog.d("handling", tag = self.TAG)        
                self.gc.control(current['GST'], current['POS'], current['duration'] / 2)
        GLog.d("control end", tag = self.TAG)
        

    def stop(self):
        self.stopped = True