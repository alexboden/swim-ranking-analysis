import re

# regex patterns
NAME_PATTERN = "/^([\u00c0-\u01ff\ufffda-zA-Z .'-]+_?[SsBbMm0-9]*)(, *[\u00c0-\u01ff\ufffda-zA-Z .'-]*)?$/g"
NAME_PATTERN_SIMPLE = "(?:[A-Z][a-z]+,\s)([A-Z][a-z]+)(?:\s)"
TIME_PATTERN = "([0-5]?[0-9]:)?[0-5][0-9]\.[0-9][0-9]"
EVENT_HEADER = "Event.*?Time"
EVENT = "[a-zA-Z].*?\s*(([0-5]?[0-9]:)?[0-5][0-9]\.[0-9][0-9]|NT)\s*\d\d\s\D*\d*"

def match_name(input_string):
    """match_name """
    match = re.search(NAME_PATTERN_SIMPLE, input_string)
    return match.group(0) if match else None

def match_all_names(input_string):
    """
    Match a string against the NAME_PATTERN_SIMPLE regular expression and return a list of
    all matched names.
    """
    it = re.finditer(NAME_PATTERN_SIMPLE, input_string)
    ret = []
    for name in it:
        ret.append(str(name.group(0)).strip())
    
    return ret

def find_event_headers(input_string):
    """
    Match a string against the EVENT_HEADER regular expression and return a list of
    all matched times.
    """
    it = re.finditer(EVENT_HEADER, input_string, flags=re.S)
    ret = []
    for name in it:
        # ret.append(str(name.group(0)).strip())
        ret.append(name.span())
    
    return ret

def seperate_entrys(input_string):
    """
    Match a string against the EVENT_HEADER regular expression and return a list of
    all matched times.
    """
    it = re.finditer(EVENT, input_string)
    ret = []
    for name in it:
        ret.append(str(name.group(0)).strip())
        # ret.append(name.span())
    
    return ret
