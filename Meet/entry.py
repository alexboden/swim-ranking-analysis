from abc import ABC, abstractmethod
import re
from config import individual_points

class Entry(ABC):
    """
    Entry class
    """
    TIME_PATTERN = "(([0-5]?[0-9]:)?[0-5][0-9]\.[0-9][0-9])|NT"

    def __init__(self):
        pass

class IndividualEntry(Entry):
    """
    Fields:
    name
    seed_time
    ranking
    score
    team_name
    """
    def __init__(self, event_string):
        """
        Takes in the string (event_string) of the entry and parses it into the different fields.
        Must be in the format of:
            "Lav 27.23  22 Ponsardin, Alice 47"
        """
        seed_time_search = re.search(Entry.TIME_PATTERN, event_string)
        
        self.team_name = event_string[0:seed_time_search.start()].strip()
        self.seed_time = event_string[seed_time_search.start():seed_time_search.end()].strip()
        
        rest_of_string = event_string[seed_time_search.end():].strip()
        self.age = rest_of_string[0:rest_of_string.find(" ")].strip()
        
        rest_of_string = rest_of_string[rest_of_string.find(" "):].strip()
        
        ranking_search = re.search("[0-9]+", rest_of_string)
        self.name = rest_of_string[0:ranking_search.start()].strip()
        self.ranking = int(rest_of_string[ranking_search.start():ranking_search.end()].strip())
        if self.ranking in individual_points:
            self.points = individual_points[self.ranking]
        else:
            self.points = 0
   
    def __str__(self):
        return f"Name : {self.name}, Seed Time: {self.seed_time}, Ranking: {self.ranking}, Points: {self.points}, Team Name: {self.team_name}, Age: {self.age} \n"

class RelayEntry(Entry):
    # team_name
    # seed_time
    # ranking
    # score 
    pass
