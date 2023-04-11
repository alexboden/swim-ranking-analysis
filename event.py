class Event:
    """Event class"""
    # Regex patterns
      
    def __init__(self, event_header_string, entry_string):
        # eventName
        # number
        # isRelay
        # entries
  
        
        if "Relay" in event_header_string:
            self.is_relay = True
        else:
            self.is_relay = False

        # split the string into a list of words
        words = event_header_string.split()
        self.number = words[1] # number ei 1

        if self.is_relay:
            self.event_name = ' '.join(words[2:8]) # eventName ei Women 50 SC Freestyle
        else:
            self.event_name = ' '.join(words[2:7]) # eventName ei Women 50 SC Freestyle

        self.entries = []

    