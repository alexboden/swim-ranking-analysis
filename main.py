from flask import Flask, render_template, request, session, jsonify, redirect, url_for 
from Meet.meet import Meet
from pypdf import PdfReader
from pymongo import MongoClient
from config import individual_points, MAX_INDIVIDUAL_EVENTS

client = MongoClient('mongodb://localhost:27017/')
db = client['swimdatabase']
collection = db['entries']

user_preferences = db['user_preferences']
user_preferences.delete_many({})
user_preferences.insert_one({'gender': 'Men'})


app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('upload.html', error='No file selected.')

        file_submission = request.files['file']

        # Check if the file is a PDF
        if file_submission.filename.split('.')[-1].lower() != 'pdf':
            return render_template('upload.html', error='File must be a PDF.')

        # Process the PDF 
        reader = PdfReader(file_submission)
        text_extract = ""

        for i in range(len(reader.pages)):
            text_extract += (reader.pages[i].extract_text())

        m = Meet(text_extract)
        
        # Clear the database
        collection.delete_many({})
        
        for event in m.events:
            for entry in event.entries:
                collection.insert_one(entry.__dict__)

        return redirect(url_for('entries'))

    # If the request method is GET, render the home page
    return render_template('upload.html')


def get_filtered_entries():
    current_gender = user_preferences.find_one()['gender']

    entries = collection.find()
    filtered_entries = []

    for entry in entries:
        if "Women" in entry['event_name'] and current_gender == "Women":
            filtered_entries.append(entry)
        if not "Women" in entry['event_name'] and current_gender == "Men":
            filtered_entries.append(entry)

    return filtered_entries

@app.route('/swap_swimmers', methods=['POST'])
def swap_swimmers():
    request_json = request.get_json()
    event, swimmer1, swimmer2 = request_json['event'], request_json['name1'], request_json['name2']

    # Find the entries for the two swimmers
    swimmer1_entry = collection.find_one({'name': swimmer1, 'event_name': event})
    swimmer2_entry = collection.find_one({'name': swimmer2, 'event_name': event})

    if swimmer1_entry is None or swimmer2_entry is None:
        return jsonify({'success': False, 'message': 'Swimmer or event not found'})

    # Swap the ranking and points values
    result1 = collection.update_one({'name': swimmer1, 'event_name': event}, {'$set': {
                                    'ranking': swimmer2_entry['ranking'], 'points': swimmer2_entry['points']}})
    result2 = collection.update_one({'name': swimmer2, 'event_name': event}, {'$set': {
                                    'ranking': swimmer1_entry['ranking'], 'points': swimmer1_entry['points']}})

    if result1.matched_count == 1 and result1.modified_count == 1 and result2.matched_count == 1 and result2.modified_count == 1:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Error updating database'})

@app.route('/delete_swimmer', methods=['POST'])
def delete_swimmer():
    request_json = request.get_json()
    event, swimmer = request_json['event'], request_json['name']
    
    status = collection.delete_one({'name': swimmer, 'event_name': event})
    if status.deleted_count == 1:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Error deleting swimmer'})


@app.route('/update_swimmer', methods=['POST'])
def update_swimmer():
    request_json = request.get_json()
    event, swimmer, ranking = request_json['event'], request_json['name'], request_json['rank']
    points = 0
    if ranking <= 16:
        points = individual_points[ranking]
    
    status = collection.update_one({'name': swimmer, 'event_name': event}, {'$set': {'points': points, 'ranking': ranking}})
    if status is not None:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Error updating swimmer'})


@app.route('/results')
def display_results():
    results = session.get('results', [])
    return render_template('results.html', results=results)


@app.route('/points_by_team')
def points_by_team():
    entries = get_filtered_entries()
    points_by_team = {} 
    for entry in entries:
        points_by_team[entry['team_name']] = points_by_team.get(entry['team_name'], 0) + entry['points'] 

    # sort the dictionary by value
    points_by_team = {k: v for k, v in sorted(points_by_team.items(), key=lambda item: item[1], reverse=True)}
    
    return points_by_team

@app.route('/entries_by_team')
def entries_by_team():
    entries = get_filtered_entries()
    ret = {}
    for entry in entries:
        if entry['team_name'] not in ret:
            ret[entry['team_name']] = {'swimmers': {}, 'points': 0,
                                    'number_of_swimmers': 0, 'over_entered_swimmers': [], 'team_name': entry['team_name']}
        if entry['name'] not in ret[entry['team_name']]['swimmers']:
            ret[entry['team_name']]['number_of_swimmers'] += 1
            ret[entry['team_name']]['swimmers'][entry['name']] = {'entries' : [], 'points': 0}

        ret[entry['team_name']]['swimmers'][entry['name']]['entries'].append(entry)
        ret[entry['team_name']]['swimmers'][entry['name']]['points'] += individual_points.get(entry['ranking'], 0)
        
        
        if len(ret[entry['team_name']]['swimmers'][entry['name']]) > MAX_INDIVIDUAL_EVENTS:
            ret[entry['team_name']]['over_entered_swimmers'].append(entry['name'])

        ret[entry['team_name']]['points'] += individual_points.get(entry['ranking'], 0)

    # sort by total points
    ret = {k: v for k, v in sorted(ret.items(), key=lambda item: item[1]['points'], reverse=True)} 
    # sort each team's swimmers by their total points ie the value of the 'points' key
    for team_name, team_data in ret.items():
        swimmers = team_data['swimmers']
        sorted_swimmers = sorted(
            swimmers.items(), key=lambda item: item[1]['points'], reverse=True)
        ret[team_name]['swimmers'] = dict(sorted_swimmers)
        
    return ret
    
@app.route('/teams')
def teams():
    entries_by_team_dict = entries_by_team()
    points_by_team_dict = points_by_team()
    gender = user_preferences.find_one()['gender']
    return render_template('teams.html', points_by_team=points_by_team_dict, entries_by_team=entries_by_team_dict, individual_points=individual_points, gender = gender)

@app.route('/entries')
def entries():
    entries = get_filtered_entries()
    entries_by_event = {}
    for entry in entries:
        entries_by_event[entry['event_name']] = entries_by_event.get(entry['event_name'], []) + [entry]
    gender = user_preferences.find_one()['gender']
    points_by_team_dict = points_by_team()
    return render_template('entries.html', events=entries_by_event, points_by_team=points_by_team_dict, gender=gender)


@app.route('/update_gender', methods=['POST'])
def update_gender():
    request_json = request.get_json()
    gender = request_json['gender']
    
    status = user_preferences.update_one({}, {'$set': {'gender': gender}})
    
    if status is not None:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Error updating swimmer'})
    
if __name__ == '__main__':
    app.run(port=3000, debug=True)
