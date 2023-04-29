from pymongo import MongoClient
from config import individual_points, MAX_INDIVIDUAL_EVENTS
import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client['swimdatabase']
collection = db['entries']

user_preferences = db['user_preferences']
user_preferences.insert_one({'gender': 'Men'})

def get_filtered_entries():
    current_gender = user_preferences.find_one()['gender']

    entries = collection.find()
    filtered_entries = []

    for entry in entries:
        print('entry: ', entry)
        if "Women" in entry['event_name'] and current_gender == "Women":
            filtered_entries.append(entry)
        if not "Women" in entry['event_name'] and current_gender == "Men":
            filtered_entries.append(entry)

    return filtered_entries


test = get_filtered_entries()
pprint.pprint(test)
