from abc import ABC, abstractmethod
import re
from config import individual_points

class Entry(ABC):
    """
    An abstract base class for entries.

    Attributes:
        TIME_PATTERN (str): A regular expression pattern for matching time strings.
    """

    TIME_PATTERN = "(([0-5]?[0-9]:)?[0-5][0-9]\.[0-9][0-9])|NT"

    @abstractmethod
    def __init__(self):
        """
        Constructor for Entry class.
        """
        pass

class IndividualEntry(Entry):
    """
    A class representing an individual entry.

    Attributes:
        team_name (str): The name of the team.
        seed_time (str): The seed time for the entry.
        age (str): The age of the entrant.
        name (str): The name of the entrant.
        ranking (int): The ranking of the entrant.
        points (int): The number of points earned by the entrant.
    """

    def __init__(self, event_string):
        """
            Constructor for IndividualEntry class.

            Args:
                event_string (str): The string representation of the entry.
                    Must be in the format of "team_name seed_time age name ranking".
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
        """
        Returns a string representation of the IndividualEntry object.

        Returns:
            str: A string representation of the IndividualEntry object.
        """
        return f"Name : {self.name}, Seed Time: {self.seed_time}, Ranking: {self.ranking}, Points: {self.points}, Team Name: {self.team_name}, Age: {self.age} \n"

class RelayEntry(Entry):
    # team_name
    # seed_time
    # ranking
    # score 
    pass
