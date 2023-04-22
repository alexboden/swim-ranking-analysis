from pypdf import PdfReader
import regex 
from Meet.entry import IndividualEntry 
from Meet.event import Event
from pprint import pprint as pprint

reader = PdfReader("usports.pdf")
number_of_pages = len(reader.pages)

page = reader.pages[0]
    
pages = ""

for i in range(number_of_pages):
    pages += (reader.pages[i].extract_text())

text = page.extract_text()
# print(text)
# print(regex.match_name(text))
# print(type(regex.match_all_names(text)))
# for name in regex.match_all_names(text):
# 	print(name)

# for event_header in regex.find_event_headers(pages):
#     print("___________________")
#     print(event_header)
#     print(pages[event_header[0]:event_header[1]])
#     event_string = pages[event_header[0]:event_header[1]]
#     e = Event(pages[event_header[0]:event_header[1]], event_string)
#     print(e)
 
total_points = {}
team_points = {}
for i in range(len(regex.find_event_headers(pages))):
    print("___________________")
    if (i != len(regex.find_event_headers(pages)) - 1):
        print(pages[regex.find_event_headers(pages)[i][0]:regex.find_event_headers(pages)[i][1]])
        event_string = pages[regex.find_event_headers(pages)[i][1]:regex.find_event_headers(pages)[i+1][0]]
        e = Event(pages[regex.find_event_headers(pages)[i][1]:regex.find_event_headers(pages)[i+1][0]], event_string)
        print(e)
        for entry in e.entries:
            total_points[entry.name] = total_points.get(entry.name, 0) + entry.points
            team_points[entry.team_name] = team_points.get(entry.team_name, 0) + entry.points
    else:
        print("lastttt")
        print(pages[regex.find_event_headers(pages)[i][0]:regex.find_event_headers(pages)[i][1]])
    

# for entry in regex.find_event_headers(pages):
# 	print("___________________")
# 	print(event_header)
# 	e = Event(text[regex.find_event_headers(text)[0][0]:regex.find_event_headers(text)[0][1]], "")

event_string = text[regex.find_event_headers(text)[0][1]:regex.find_event_headers(text)[1][0]]

e = Event(text[regex.find_event_headers(text)[0][0]:regex.find_event_headers(text)[0][1]], event_string)


for entry in e.entries:
    total_points[entry.name] = total_points.get(entry.name, 0) + entry.points
    team_points[entry.team_name] = team_points.get(entry.team_name, 0) + entry.points

pprint(total_points)
pprint(team_points)	
