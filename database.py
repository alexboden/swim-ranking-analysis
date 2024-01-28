# database.py
from pymongo import MongoClient
import pandas as pd
import datetime as dt

class Database:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['swimdatabase']
        self.collection = self.db['entries']
        self.user_preferences = self.db['user_preferences']
        self.clear_database()
    
    def clear_database(self):
            self.collection.delete_many({})
            self.user_preferences.delete_many({})
            self.user_preferences.insert_one({'gender': 'Men'})

    def load_from_csv(self, path):
            self.clear_database()
            df = self.read_csv(path)
            records = df.to_dict(orient='records')
            self.collection.insert_many(records) 
    
    def export_to_csv(self):
            cursor = self.collection.find()
            df = pd.DataFrame(list(cursor))
            # drop the _id column
            df = df.drop('_id', axis=1)
            cur_date = dt.datetime.now()
            formatted_datetime = cur_date.strftime("%Y-%m-%d %H:%M")
            name = "Swim Analysis:" + formatted_datetime + ".csv"
            df.to_csv(name, index=False)
    
    def get_current_gender(self):
        return self.user_preferences.find_one()['gender']

    def get_filtered_entries(self):
        current_gender = self.user_preferences.find_one()['gender']

        entries = self.collection.find()
        filtered_entries = []

        # TODO Clean this up
        for entry in entries:
            if "Women" in entry['event_name'] and current_gender == "Women":
                filtered_entries.append(entry)
            if "Women" not in entry['event_name'] and current_gender == "Men":
                filtered_entries.append(entry)

        return filtered_entries 

 
