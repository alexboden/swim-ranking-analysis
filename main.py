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

for entry in regex.seperate_entrys(text[regex.find_event_headers(text)[0][1]:regex.find_event_headers(text)[1][0]]):
	print("___________________")
	print(entry)

event_string = text[regex.find_event_headers(text)[0][1]:regex.find_event_headers(text)[1][0]]

print(e.event_name)
print(e.is_relay)
print(e.number)

print(event_string)

e = IndividualEntry("Lav 27.23  22 Ponsardin, Alice 47") 

print(e.name)
print(e.seed_time)
print(e.age)
print(e.ranking)
print(e.team_name)
