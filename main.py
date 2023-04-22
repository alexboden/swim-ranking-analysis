from pypdf import PdfReader
from Meet.entry import IndividualEntry 
from Meet.event import Event
from Meet.meet import Meet
from pprint import pprint as pprint
import logging

# Set up logging file
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('log/out.log')
logger.addHandler(file_handler)

# File to analyze
reader = PdfReader("usports.pdf")
text_extract = ""

for i in range(len(reader.pages)):
    text_extract += (reader.pages[i].extract_text())


# for entry in e.entries:
#     total_points[entry.name] = total_points.get(entry.name, 0) + entry.points
#     team_points[entry.team_name] = team_points.get(entry.team_name, 0) + entry.points

# pprint(total_points)
# pprint(team_points)	

m = Meet(text_extract)

for event in m.events:
    logger.info(event)

logger.warning('This is a warning message.')

print(m.events[1])
