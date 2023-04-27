from pymongo import MongoClient
from config import individual_points, MAX_INDIVIDUAL_EVENTS
import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client['swimdatabase']
collection = db['entries']


def entries_by_team():
    entries = db['entries'].find()
    ret = {}
    for entry in entries:
        if entry['team_name'] not in ret:
            ret[entry['team_name']] = {'swimmers': {}, 'points': 0,
                                       'number_of_swimmers': 0, 'over_entered_swimmers': [], 'team_name': entry['team_name']}
        if entry['name'] not in ret[entry['team_name']]['swimmers']:
            ret[entry['team_name']]['number_of_swimmers'] += 1
            ret[entry['team_name']]['swimmers'][entry['name']] = []
            
        ret[entry['team_name']]['swimmers'][entry['name']].append(entry)
        if len(ret[entry['team_name']]['swimmers'][entry['name']]) > MAX_INDIVIDUAL_EVENTS:
            print(entry['name'])
            ret[entry['team_name']]['over_entered_swimmers'].append(entry['name'])

        if entry['ranking'] < len(individual_points) + 1:
            ret[entry['team_name']]['points'] += individual_points[entry['ranking']]

    return ret

test = entries_by_team()
pprint.pprint(test)
