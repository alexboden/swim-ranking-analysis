from Meet.entry import Entry

class Swimmer:
    """
    Represents a swimmer in a meet.
    """

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.points = 0
        self.entries = []

    def add_to_entries(self, entry):
        self.entries += [entry]
        self.points += entry.points
