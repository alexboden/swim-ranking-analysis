from pypdf import PdfReader
import regex 
from Meet.entry import IndividualEntry 
from Meet.event import Event

reader = PdfReader("usports.pdf")
number_of_pages = len(reader.pages)

page = reader.pages[0]
	
text = page.extract_text()
# print(text)
# print(regex.match_name(text))
# print(type(regex.match_all_names(text)))
# for name in regex.match_all_names(text):
# 	print(name)

for event_header in regex.find_event_headers(text):
	print("___________________")
	print(event_header)


for entry in regex.find_event_headers(text):
	print("___________________")
	print(event_header)
	e = Event(text[regex.find_event_headers(text)[0][0]:regex.find_event_headers(text)[0][1]], "")

event_string = text[regex.find_event_headers(text)[0][1]:regex.find_event_headers(text)[1][0]]

e = Event(text[regex.find_event_headers(text)[0][0]:regex.find_event_headers(text)[0][1]], event_string)

print(e)
total_points = {}
team_points = {}

for entry in e.entries:
	total_points[entry.name] = total_points.get(entry.name, 0) + entry.points
	team_points[entry.team_name] = team_points.get(entry.team_name, 0) + entry.points

print(total_points)
print(team_points)	
