'''
    This file contain the demonstration of using pyautogui with feeding frenzy game
'''
from InputFeeder import InputFeeder



class GameController:
    def __init__(self, config):
        self.inputFeeder = InputFeeder()
        self.lastGesture = "w"
        self.config = {}
        for gesture in config:
            self.config[gesture] = {"control": config[gesture], "prev": (0,0), "curr": (0,0)}

    def __track__(self, gesture, center):
        print(gesture, center, self.lastGesture)
        #clear other gestures
        for ges in self.config:
            if(ges == gesture): continue
            self.config[ges]['prev'] = self.config[ges]['curr'] = (0,0)

        # todo update this condition and support "sensitivity setting" (less sensitive means checking for more prev gestures to be the same as current to make an action)
        if(self.lastGesture != gesture): #* highest sensitivity, only counts one prev gesture to be same as current to take an action (this is more noisy) 
            self.config[gesture]['prev'] = self.config[gesture]['curr'] = center
            return

        if (not gesture in self.config):
            return
        self.config[gesture]["prev"] = self.config[gesture]["curr"]
        self.config[gesture]["curr"] = center

    def control(self, gesture, center):
        if(gesture == "NO SHAPE"):
            return
        self.__track__(gesture, center)
        g_config = self.config[gesture]
        if(g_config["control"] == "moving"):
            self.inputFeeder.move(g_config["prev"], g_config["curr"])

        elif(g_config["control"] == "right click"):
            self.inputFeeder.rightClick()

        elif(g_config["control"] == "left click"):
            self.inputFeeder.leftClick()

        elif(g_config["control"] == "drag right"):
            self.inputFeeder.dragRightClick(g_config["prev"], g_config["curr"])

        elif(g_config["control"] == "drag left"):
            self.inputFeeder.dragLeftClick(g_config["prev"], g_config["curr"])

        elif(g_config["control"] == "esc"):
            self.inputFeeder.pressChars(['esc'])

        self.lastGesture = gesture


if __name__ == "__main__":
    from ConfigReader import ConfigReader
    gc = GameController(config=ConfigReader.default())
    print(gc.config)