from abc import ABC, abstractmethod

class Entry(ABC):

    TIME_PATTERN = "([0-5]?[0-9]:)?[0-5][0-9]\.[0-9][0-9]"

    def __init__(self):
        pass

class IndividualEntry(Entry):
    # name
    # seed time
    # ranking
    # score
    def __init__(self, swimmer_name, seed_time, ranking, score):
        self.swimmer_name = swimmer_name
        self.seed_time = seed_time
        self.ranking = ranking
        self.score = score

class RelayEntry(Entry):
    # team_name
    # seed_time
    # ranking
    # score 
    pass
