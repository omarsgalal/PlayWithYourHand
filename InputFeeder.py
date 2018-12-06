import pyautogui as pya


class InputFeeder:
    def __init__(self):
        pass

    def __dx__(self, prev, current):
        return current[0] - prev[0]
    
    def __dy__(self, prev, current):
        return current[1] - prev[1]

    def move(self, prev, current):
        dx, dy = self.__dx__(prev, current), self.__dy__(prev, current)
        print("input feeder: ", dx,dy)
        pya.moveRel(xOffset=dx*10, yOffset=dy*10, duration=0.1)

    def dragLeftClick(self, prev, current):
        dx, dy = self.__dx__(prev, current), self.__dy__(prev, current)
        pya.dragRel(xOffset=dx, yOffset=dy, duration=0.001)

    def dragRightClick(self, prev, current):
        dx, dy = self.__dx__(prev, current), self.__dy__(prev, current)
        pya.dragRel(xOffset=dx, yOffset=dy, duration=0.001, button='right')


    def scrollH(self, prev, current):
        dx = self.__dx__(prev, current)
        pya.scroll(clicks=dx)

    def scrollV(self, prev, current):
        dy = self.__dy__(prev, current)
        pya.scroll(clicks=dy)

    def pressChars(self, chars):
        for c in chars:
            pya.press(c)

    def leftClick(self):
        pya.click()

    def rightClick(self):
        pya.rightClick()
    
