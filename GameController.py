from InputFeeder import InputFeeder
from ControlActions import *
from Gestures import NO_GST
from AppLogger import ImageLogger as ILog, GeneralLogger as GLog
from utils import showImages, timeMessage
from cv2 import getTickCount, getTickFrequency

class GameController:
    TAG = "GameController"
    def __init__(self, config, sensitivity = 1): # sensitivity = 1 is largest sensitivity, more sensitivity value means less sensitivity
        self.sensitivity = sensitivity
        self.inputFeeder = InputFeeder()
        self.config = {}
        for gesture in config:
            self.config[gesture] = {"control": config[gesture], "prev": (0,0), "curr": (0,0)}
        #self.config[NO_GST] = {"control": NO_ACTION, "prev": (0,0), "curr": (0,0)}
        self.lastGesture = NO_GST
        self.prevSensitivityGes = NO_GST
        self.sameGesCount = 0

    def __track__(self, gesture, center):
        if(self.lastGesture != gesture): # first time to see this gesture, current data is garbage and should be recalculated again upon this moment
            self.config[gesture]['prev'] = self.config[gesture]['curr'] = center
            return

        self.config[gesture]["prev"] = self.config[gesture]["curr"]
        self.config[gesture]["curr"] = center

    def __shouldConsidered__(self, gesture):
        # (less sensitive means checking for more prev gestures to be the same as current to make an action)
        #* highest sensitivity, only counts one prev gesture to be same as current to take an action (this is more noisy)
        if(gesture == self.prevSensitivityGes):
            self.sameGesCount += 1
            if(self.sameGesCount == self.sensitivity):
                # found same gesture sensitivity value times, so consider it as true recognition, and start counting again 
                self.sameGesCount = 0
                return True
            return False
        
        self.sameGesCount = 0 # count again, the chain is broken with new gesture
        self.prevSensitivityGes = gesture
        return False

    def control(self, gesture, center = (0,0), dt = 0.2):
        if(not self.__shouldConsidered__(gesture)):
            GLog.d("gesture '{}' found but didn't considered due to sensitivity option".format(gesture), tag=self.TAG)
            return
        self.__track__(gesture, center)
        g_config = self.config[gesture] # config of this gesture
        
        e1 = getTickCount()
        # to detect: 
        #   'key down': config[gesture] == action and lastGesture != gesture
        #   'key up': config[lastGesture] == action and lastGesture != gesture
        #   'hold': config[gesture] == action
        if(g_config["control"] == MOVE):
            self.inputFeeder.move(g_config["prev"], g_config["curr"], duration = dt)
            GLog.o(timeMessage("controlling", e1), tag="TIME")
        

        elif(g_config["control"] == RIGHT_CLICK and self.lastGesture != gesture):# for first time only [press when 'key down']
            GLog.o("right mouse click", tag=self.TAG)
            self.inputFeeder.rightClick()
            GLog.o(timeMessage("controlling", e1), tag="TIME")
        

        elif(g_config["control"] == LEFT_CLICK and self.lastGesture != gesture):
            GLog.o("left mouse click", tag=self.TAG)
            self.inputFeeder.leftClick()
            GLog.o(timeMessage("controlling", e1), tag="TIME")
        

        elif(g_config["control"] == DRAG_RIGHT_CLICK):
            GLog.o("dragging with right click", tag=self.TAG)
            self.inputFeeder.dragRightClick(g_config["prev"], g_config["curr"])
            GLog.o(timeMessage("controlling", e1), tag="TIME")
        

        elif(g_config["control"] == DRAG_LEFT_CLICK):
            GLog.o("dragging with left click", tag=self.TAG)
            self.inputFeeder.dragLeftClick(g_config["prev"], g_config["curr"])
            GLog.o(timeMessage("controlling", e1), tag="TIME")
        

        elif(g_config["control"] == ESCAPE and self.lastGesture != gesture):
            GLog.o("escape press", tag=self.TAG)
            self.inputFeeder.pressChars(['esc'])
            GLog.o(timeMessage("controlling", e1), tag="TIME")
        
        else: 
            GLog.d("gesture '{}' is not found in config file or already pressed".format(gesture), tag=self.TAG)
        self.lastGesture = gesture



if __name__ == "__main__":
    from ConfigReader import ConfigReader
    import Gestures
    gc = GameController(config=ConfigReader.default(), sensitivity=3)
    print(gc.config)

    # simulate and test sensitivity and key down
    for _ in range(16):
        gc.control(Gestures.FIST)
    for _ in range(3):
        gc.control(Gestures.KNIFE)
        gc.control(Gestures.KNIFE)
        gc.control(Gestures.KNIFE)
        gc.control(Gestures.KNIFE)
        gc.control(Gestures.NO_GST)
        gc.control(Gestures.NO_GST)
        gc.control(Gestures.NO_GST)
        gc.control(Gestures.NO_GST)
        gc.control(Gestures.NO_GST)
        gc.control(Gestures.KNIFE)
        gc.control(Gestures.KNIFE)
        gc.control(Gestures.KNIFE)
        gc.control(Gestures.KNIFE)