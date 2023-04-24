from Meet.entry import IndividualEntry, RelayEntry
import re

class Event:
    """
    A class representing a single event in a meet.

    Attributes:
    -----------
    event_name : str
        The name of the event.
    number : str
        The number of the event.
    is_relay : bool
        Whether the event is a relay event or not.
    entries : List[Union[IndividualEntry, RelayEntry]]
        A list of the entries for the event.
	gender : str
		Gender that is competing in the event.
    Methods:
    --------
    __init__(self, event_header_string: str, entry_string: str) -> None
        Initializes a new instance of the Event class.
    __separate_entries_individual(self, input_string: str) -> List[str]
        Returns a list of individual entry strings parsed from the input string.
    __str__(self) -> str
        Returns a string representation of the event.
    """
    
    # Regex patterns
    EVENT_PATTERN = "[a-zA-Z].*?\s*(([0-5]?[0-9]:)?[0-5][0-9]\.[0-9][0-9]|NT)\s*\d\d\s\D*\d*"

    def __init__(self, event_header_string, entry_string):
        if "Relay" in event_header_string:
            self.is_relay = True
            self.event_name = ''
            self.entries = []
            self.number = 0
            return
        else:
            self.is_relay = False

        if "Women" in event_header_string:
            self.gender = "Women"
        else:
            self.gender = "Men"
        
        # split the string into a list of words
        words = event_header_string.split()
        self.number = words[1] # number ei 1

        if self.is_relay:
            self.event_name = ' '.join(words[2:8]) # eventName ei Women 200 SC Freestyle Relay
        else:
            self.event_name = ' '.join(words[2:7]) # eventName ei Women 50 SC Freestyle

        self.entries = []
        entry_strings = self.__separate_entries_individual(entry_string)
        for entry_string in entry_strings:
            if "_" in entry_string:
                continue
            self.entries.append(IndividualEntry(entry_string, self.event_name))

    def __separate_entries_individual(self, input_string):
        """
        Returns a list of individual entry strings parsed from the input string.

        Parameters:
        -----------
        input_string : str
            The string to parse.

        Returns:
        --------
        List[str]
            A list of individual entry strings.
        """
        it = re.finditer(Event.EVENT_PATTERN, input_string)
        ret = []
        for name in it:
            ret.append(str(name.group(0)).strip())
        
        return ret

    def __str__(self) -> str:
        """
        Returns a string representation of the event.

        Returns:
        --------
        str
            The string representation of the event.
        """
        s = f"Event: {self.number} {self.event_name} \n"
        for entry in self.entries:
            s += str(entry)
        return s
