from matplotlib import colors


class Type:
    next_value = 0

    def __init__(self, name, color, probability, tolerance=None):
        self.name = name
        self.value = Type.next_value
        Type.next_value += 1
        self.color = colors.to_rgb(color)
        self.probability = probability
        self.tolerance = tolerance

    def __eq__(self, other_type: object) -> bool:
        return self.value == other_type.value
