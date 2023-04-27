from flask import Flask, render_template, request, session, jsonify, redirect, url_for 
from Meet.meet import Meet
from pypdf import PdfReader
from pymongo import MongoClient
from config import individual_points, MAX_INDIVIDUAL_EVENTS

client = MongoClient('mongodb://localhost:27017/')
db = client['swimdatabase']
collection = db['entries']


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
        reader = PdfReader(file_submission.filename)
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
    entries = db['entries'].find()
    points_by_team = {} 
    for entry in entries:
        points_by_team[entry['team_name']] = points_by_team.get(entry['team_name'], 0) + entry['points'] 

    # sort the dictionary by value
    points_by_team = {k: v for k, v in sorted(points_by_team.items(), key=lambda item: item[1], reverse=True)}
    
    return points_by_team

@app.route('/entries_by_team')
def entries_by_team():
    entries = db['entries'].find()
    ret = {}
    for entry in entries:
        if entry['team_name'] not in ret:
            ret[entry['team_name']] = {'swimmers': {}, 'points': 0,
                                    'number_of_swimmers': 0, 'over_entered_swimmers': [], 'team_name': entry['team_name']}
        if entry['name'] not in ret[entry['team_name']]['swimmers']:
            ret[entry['team_name']]['number_of_swimmers'] += 1
            ret[entry['team_name']]['swimmers'][entry['name']] = list()

        ret[entry['team_name']]['swimmers'][entry['name']].append(entry)
        if len(ret[entry['team_name']]['swimmers'][entry['name']]) > MAX_INDIVIDUAL_EVENTS:
            ret[entry['team_name']]['over_entered_swimmers'].append(entry['name'])

        if entry['ranking'] < len(individual_points) + 1:
            ret[entry['team_name']]['points'] += individual_points[entry['ranking']]

    
    return ret
    
@app.route('/teams')
def teams():
    entries_by_team_dict = entries_by_team()
    points_by_team_dict = points_by_team()
    return render_template('teams.html', points_by_team=points_by_team_dict, entries_by_team=entries_by_team_dict, individual_points=individual_points)

@app.route('/entries')
def entries():
    entries = db['entries'].find()
    entries_by_event = {}
    for entry in entries:
        entries_by_event[entry['event_name']] = entries_by_event.get(entry['event_name'], []) + [entry]
    
    points_by_team_dict = points_by_team()
    return render_template('broken_out_by_entry.html', events=entries_by_event, points_by_team=points_by_team_dict)


if __name__ == '__main__':
    app.run(port=3001, debug=True)