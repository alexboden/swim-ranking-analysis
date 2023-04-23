from pypdf import PdfReader
from Meet.entry import IndividualEntry 
from Meet.event import Event
from Meet.meet import Meet
import logging, datetime
from pprint import pprint as pprint

# Set up logging file
logger = logging.getLogger()
logger.setLevel(logging.INFO)
now = datetime.datetime.now()
log_file_name = f"log/{now.strftime('%Y-%m-%d_%H-%M-%S')}.log"
file_handler = logging.FileHandler(log_file_name)
logger.addHandler(file_handler)

# File to analyze
reader = PdfReader("oua.pdf")
text_extract = ""

for i in range(len(reader.pages)):
    text_extract += (reader.pages[i].extract_text())


# for entry in e.entries:
#     total_points[entry.name] = total_points.get(entry.name, 0) + entry.points
#     team_points[entry.team_name] = team_points.get(entry.team_name, 0) + entry.points

# pprint(total_points)
# pprint(team_points)	

m = Meet(text_extract)

# for event in m.events:
#     logger.info(event.event_name)

# for event in m.events:
#     logger.info(event)

x = m.get_swimmer_breakdown("Men")

new_x = {}

for key in x:
    logger.info(x[key].name + " " + str(x[key].points) + " " + str(len(x[key].entries)))
    for entry in x[key].entries:
        logger.info("           " + str(entry).strip())
    new_x[x[key].name] = x[key].points

new_x = sorted(new_x.items(), key=lambda x: x[1], reverse=True)
 
pprint(new_x)
