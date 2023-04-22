from Meet.entry import IndividualEntry, RelayEntry
import re

class Event:
    """Event class"""
    # Regex patterns
    EVENT = "[a-zA-Z].*?\s*(([0-5]?[0-9]:)?[0-5][0-9]\.[0-9][0-9]|NT)\s*\d\d\s\D*\d*"
    def __init__(self, event_header_string, entry_string):
        # eventName
        # number
        # isRelay
        # entries
        # gender
        
        if "Relay" in event_header_string:
            self.is_relay = True
            self.event_name = 'bruh'
            self.entries = []
            self.number = 0
            return
        else:
            self.is_relay = False

        # split the string into a list of words
        words = event_header_string.split()
        self.number = words[1] # number ei 1

        if self.is_relay:
            self.event_name = ' '.join(words[2:8]) # eventName ei Women 200 SC Freestyle Relay
        else:
            self.event_name = ' '.join(words[2:7]) # eventName ei Women 50 SC Freestyle

        self.entries = []
        entry_strings = self.__seperate_entrys_individual(entry_string)
        for entry_string in entry_strings:
            print(entry_string)
            self.entries.append(IndividualEntry(entry_string))

    def __seperate_entrys_individual(self, input_string):
        """
        Match a string against the EVENT regular expression and return a list of
        all matched event.
        """
        it = re.finditer(Event.EVENT, input_string)
        ret = []
        for name in it:
            ret.append(str(name.group(0)).strip())
        
        return ret

    def __str__(self) -> str:
        s = f"Event: {self.event_name} {self.number} \n"
        for entry in self.entries:
            s += str(entry)
        return s
