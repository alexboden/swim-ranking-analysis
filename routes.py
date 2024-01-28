import datetime as dt
from flask import render_template, request, jsonify, redirect, url_for, send_file
from Meet.meet import Meet
from config import individual_points, MAX_INDIVIDUAL_EVENTS
import pandas as pd
from pypdf import PdfReader
from flask import Blueprint
from database import Database

bp = Blueprint('routes', __name__)
db = Database()

@bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('upload.html', error='No file selected.')

        file_submission = request.files['file']

        # Check the file type
        file_type = file_submission.filename.split('.')[-1].lower()

        if file_type == 'pdf':
            # Process the PDF
            reader = PdfReader(file_submission)
            text_extract = ""

            for i in range(len(reader.pages)):
                text_extract += (reader.pages[i].extract_text())

            m = Meet(text_extract)
            
            # Clear the database
            db.collection.delete_many({})

            for event in m.events:
                for entry in event.entries:
                    db.collection.insert_one(entry.__dict__)

        elif file_type == 'csv':
            db.load_from_csv(file_submission)
        else:
            return render_template('upload.html', error='File must be a PDF or CSV.')

        return redirect(url_for('routes.entries'))

    return render_template('upload.html')


@bp.route('/swap_swimmers', methods=['POST'])
def swap_swimmers():
    request_json = request.get_json()
    event, swimmer1, swimmer2 = request_json['event'], request_json['name1'], request_json['name2']

    # Find the entries for the two swimmers
    swimmer1_entry = db.collection.find_one({'name': swimmer1, 'event_name': event})
    swimmer2_entry = db.collection.find_one({'name': swimmer2, 'event_name': event})

    if swimmer1_entry is None or swimmer2_entry is None:
        return jsonify({'success': False, 'message': 'Swimmer or event not found'})

    # Swap the ranking and points values
    result1 = db.collection.update_one({'name': swimmer1, 'event_name': event}, {'$set': { 'ranking': swimmer2_entry['ranking'], 'points': swimmer2_entry['points']}})
    result2 = db.collection.update_one({'name': swimmer2, 'event_name': event}, {'$set': { 'ranking': swimmer1_entry['ranking'], 'points': swimmer1_entry['points']}})

    if result1.matched_count == 1 and result1.modified_count == 1 and result2.matched_count == 1 and result2.modified_count == 1:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Error updating database'})


@bp.route('/delete_swimmer', methods=['POST'])
def delete_swimmer():
    request_json = request.get_json()
    event, swimmer = request_json['event'], request_json['name']

    # Get all swimmers in the event
    event_data = db.collection.find({'event_name': event}).sort('points', -1)

    # Determine the current rank and points of the swimmer to be deleted
    swimmer_data = db.collection.find_one({'name': swimmer, 'event_name': event})
    current_rank = swimmer_data['ranking']

    # Delete the swimmer
    status = db.collection.delete_one({'name': swimmer, 'event_name': event})
    if status.deleted_count == 1:
        # Update the rankings and points of the remaining swimmers
        for swimmer in event_data:
            if swimmer['ranking'] > current_rank:
                # Update the rank of the swimmer
                new_rank = swimmer['ranking'] - 1
                db.collection.update_one({'name': swimmer['name'], 'event_name': event}, {'$set': {'ranking': new_rank}})
                # Update the points of the swimmer
                new_points = individual_points.get(new_rank, 0)
                db.collection.update_one({'name': swimmer['name'], 'event_name': event}, {'$set': {'points': new_points}})
            else:
                break  # Stop updating swimmers once the deleted swimmer's rank is reached

        return jsonify({'success': True})

    else:
        return jsonify({'success': False, 'message': 'Error deleting swimmer'})


@bp.route('/update_swimmer', methods=['POST'])
def update_swimmer():
    request_json = request.get_json()
    event, swimmer, ranking = request_json['event'], request_json['name'], request_json['rank']
    
    
    points = 0
    if ranking in individual_points:
        points = individual_points[ranking]

    status = db.collection.update_one({'name': swimmer, 'event_name': event}, {'$set': {'points': points, 'ranking': ranking}})

    if status is not None:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Error updating swimmer'})


@bp.route('/points_by_team')
def points_by_team():
    entries = db.get_filtered_entries()
    points_by_team = {}
    for entry in entries:
        points_by_team[entry['team_name']] = points_by_team.get(
            entry['team_name'], 0) + entry['points']

    # sort the dictionary by value and return it
    return {k: v for k, v in sorted( points_by_team.items(), key=lambda item: item[1], reverse=True)}


@bp.route('/entries_by_team')
def entries_by_team():
    entries = db.get_filtered_entries()
    ret = {}
    for entry in entries:
        if entry['team_name'] not in ret:
            ret[entry['team_name']] = {'swimmers': {}, 'points': 0, 'number_of_swimmers': 0, 'over_entered_swimmers': [], 'team_name': entry['team_name']}
        if entry['name'] not in ret[entry['team_name']]['swimmers']:
            ret[entry['team_name']]['number_of_swimmers'] += 1
            ret[entry['team_name']]['swimmers'][entry['name']] = {'entries': [], 'points': 0}

        ret[entry['team_name']]['swimmers'][entry['name']]['entries'].append(entry)
        
        ret[entry['team_name']]['swimmers'][entry['name']]['points'] += individual_points.get(entry['ranking'], 0)

        if len(ret[entry['team_name']]['swimmers'][entry['name']]) > MAX_INDIVIDUAL_EVENTS:
            ret[entry['team_name']]['over_entered_swimmers'].append(
                entry['name'])

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


@bp.route('/teams')
def teams():
    entries_by_team_dict = entries_by_team()
    points_by_team_dict = points_by_team()
    gender = db.get_current_gender()
    return render_template('teams.html', points_by_team=points_by_team_dict, entries_by_team=entries_by_team_dict, individual_points=individual_points, gender=gender)


@bp.route('/entries')
def entries():
    entries = db.get_filtered_entries()
    entries_by_event = {}
    for entry in entries:
        entries_by_event[entry['event_name']] = entries_by_event.get(
            entry['event_name'], []) + [entry]
    gender = db.get_current_gender()
    points_by_team_dict = points_by_team()
    return render_template('entries.html', events=entries_by_event, points_by_team=points_by_team_dict, gender=gender)


@bp.route('/update_gender', methods=['POST'])
def update_gender():
    request_json = request.get_json()
    gender = request_json['gender']

    status = db.user_preferences.update_one({}, {'$set': {'gender': gender}})

    if status is not None:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Error updating swimmer'})


@bp.route('/export', methods=['GET'])
def export():
    file_path = db.export_to_csv()
    return send_file(file_path, mimetype='text/csv', as_attachment=True)

