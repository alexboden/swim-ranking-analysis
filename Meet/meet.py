import regex
from Meet.event import Event
from Meet.swimmer import Swimmer

class Meet:
    """
    A class representing a meet.

    Attributes:
    - events (list of Event objects): the list of events in the meet

    Methods:
    - __init__(self, extracted_text): initializes a Meet object with the given extracted text
    - __str__(self): returns a string representation of the Meet object
    """

    def __init__(self, extracted_text):
        """
        Initializes a Meet object with the given extracted text.

        Args:
        - extracted_text (str): the extracted text to parse and extract event information from

        Returns:
        - None
        """
        self.events = []
        event_header_strings = regex.find_event_headers(extracted_text)

        for i in range(len(event_header_strings)):
            if (i != len(event_header_strings) - 1):
                event_header_string = extracted_text[event_header_strings[i][0]:event_header_strings[i][1]]
                if ("Relay" in event_header_string):
                    continue
                e = Event(event_header_string, extracted_text[event_header_strings[i][1]:event_header_strings[i+1][0]])
                
                duplicate = False
                for event in self.events:
                    if (event.number == e.number):
                        event.entries += e.entries
                        duplicate = True
                        break
                if not duplicate:
                    self.events += [e]

            else:
                continue
                # print(extracted_text[regex.find_event_headers(extracted_text)[i][0]:regex.find_event_headers(extracted_text)[i][1]])

    
    def get_swimmer_breakdown(self, gender):
        SwimmerBreakdown = {}
        for event in self.events:
            if event.gender != gender:
                continue
            for entry in event.entries:
                if entry.name not in SwimmerBreakdown:
                    SwimmerBreakdown[entry.name] = Swimmer(entry.name, gender)
                
                SwimmerBreakdown[entry.name].add_to_entries(entry)
        return SwimmerBreakdown
            
            
    def __str__(self):
        """
        Returns a string representation of the Meet object.

        Returns:
        - str: the string representation of the Meet object
        """
        return f'Meet \nNumber of events: {len(self.events)}'
