class ConfigReader:
    def __init__(self):
        pass


    @classmethod
    def fromPath(cls, path):
        return {}

    @classmethod
    def default(cls):
        return {
            "PALM": "moving",
            "FIST": "left click",
            "KNIFE": "esc",
            "ZERO": "right click",
        }