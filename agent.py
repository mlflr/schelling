from constants import UNHAPPY_TYPE


class Agent:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.happy = True

    def is_type(self, type):
        return self.type == type

    def get_colour(self):
        return self.type.color if self.happy else UNHAPPY_TYPE.color

    def get_type_value(self):
        return self.type.value if self.happy else UNHAPPY_TYPE.value
