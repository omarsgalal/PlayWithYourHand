from ControlActions import *
from Gestures import *
class ConfigReader:
    def __init__(self):
        pass


    @classmethod
    def fromPath(cls, path):
        return {}

    @classmethod
    def default(cls):
        return {
            PALM: MOVE,
            FIST: LEFT_CLICK,
            KNIFE: ESCAPE,
            ZERO: RIGHT_CLICK,
            NO_GST: NO_ACTION,
        }