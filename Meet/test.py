import re
import entry
import config
# EVENT_PATTERN = "(X?\d{1,2}:\d{2}\.\d{2})\s+(\d+)\s+([A-Z]+)\s+((?:[A-Za-z'-]+\s?)+),\s+([A-Za-z'-]+)\s+(\d+)"
# EVENT_PATTERN = r"([A-Z]+)\s+(\d{1,2}:\d{2}\.\d{2})\s+(\d+)\s+([A-Za-z'-]+),\s+([A-Za-z'-]+)\s+Q?\s+(\d+)"
EVENT_PATTERN = r"([A-Z]+)\s+(\d{1,2}:\d{2}\.\d{2})\s+(\d+)\s+([A-Za-z'-]+),\s+([A-Za-z'-]+)(\s+Q)?( \d+)"

# input_string = 'UT 2:13.66  2 Mollin, Nina Q 1\nWES 2:15.45  5 Rennie, Ella 2\n UT 2:15.62  3 Klenk, Haley Q 3 UT 2:16.86  3 Russell, Shannon Q 4 UG 2:19.98  1 Casasanta, Alanna Q 5 UT 2:20.11  3 Guan, Tina Q 6 WES 2:20.59  3 Macleod, Claire Q 7Brock University Pool - Site License HY -TEKs MEET MANAGER 8.0 - 9:47 PM  2024-02-12  Page 17 Ontario University Championships 2024 - 20240216 to 2024-0218 Psych Sheet'

# read from "regex.txt"
input_string = ""
with open("regex.txt", "r") as f:
	input_string = f.read()


it = re.finditer(EVENT_PATTERN, input_string)
ret = []
for name in it:
	ret.append(str(name.group(0)).strip())
 
# print(ret)

for s in ret:
	print(entry.IndividualEntry(s, "event"))


