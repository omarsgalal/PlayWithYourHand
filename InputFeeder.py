import pyautogui as pya
from AppLogger import GeneralLogger as GLog
pya.FAILSAFE = False
class InputFeeder:
    TAG = "InputFeeder"
    def __init__(self):
        pass

    def __dx__(self, prev, current):
        return current[0] - prev[0]
    
    def __dy__(self, prev, current):
        return current[1] - prev[1]

    def move(self, prev, current, duration = 0):
        dx, dy = self.__dx__(prev, current), self.__dy__(prev, current)
        GLog.d("dx= {}, dy= {}".format(dx, dy), tag=self.TAG)
        pya.moveRel(xOffset=dx*duration*50, yOffset=dy*duration*50, duration=0.05)

    def dragLeftClick(self, prev, current):
        dx, dy = self.__dx__(prev, current), self.__dy__(prev, current)
        GLog.d("dx= {}, dy= {}".format(dx, dy), tag=self.TAG)
        pya.dragRel(xOffset=dx*3, yOffset=dy*3, duration=0.001)

    def dragRightClick(self, prev, current):
        dx, dy = self.__dx__(prev, current), self.__dy__(prev, current)
        GLog.d("dx= {}, dy= {}".format(dx, dy), tag=self.TAG)
        pya.dragRel(xOffset=dx, yOffset=dy, duration=0.001, button='right')


    def scrollH(self, prev, current):
        dx = self.__dx__(prev, current)
        GLog.d("dx= {}".format(dx), tag=self.TAG)
        pya.scroll(clicks=dx)

    def scrollV(self, prev, current):
        dy = self.__dy__(prev, current)
        GLog.d("dy= {}".format(dy), tag=self.TAG)
        pya.scroll(clicks=dy)

    def pressChars(self, chars):
        for c in chars:
            pya.press(c)

    def leftClick(self):
        pya.click()

    def rightClick(self):
        pya.rightClick()
    