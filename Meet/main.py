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


