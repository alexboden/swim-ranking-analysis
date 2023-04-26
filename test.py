from flask import Flask, render_template, request, session, jsonify, redirect, url_for 
from Meet.meet import Meet
from pypdf import PdfReader
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['swimdatabase']
collection = db['entries']


app = Flask(__name__)
app.debug = True

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('home.html', error='No file selected.')

        file_submission = request.files['file']

        # Check if the file is a PDF
        if file_submission.filename.split('.')[-1].lower() != 'pdf':
            return render_template('home.html', error='File must be a PDF.')

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
        # results = m.get_team_breakdown("Men")
        # entries = db['entries'].find()

        return redirect(url_for('entries'))

    # If the request method is GET, render the home page
    return render_template('home.html')

# Define the route for displaying the results

@app.route('/entries')
def entries():
    entries = db['entries'].find()
    entries_by_event = {}
    for entry in entries:
        entries_by_event[entry['event_name']] = entries_by_event.get(entry['event_name'], []) + [entry]
    return render_template('broken_out_by_entry.html', events=entries_by_event)


@app.route('/swap_swimmers', methods=['POST'])
def swap_swimmers():
    request_json = request.get_json()
    event = request_json['event']
    swimmer1 = request_json['name1']
    swimmer2 = request_json['name2']

    # Find the entries for the two swimmers
    swimmer1_entry = collection.find_one({'name': swimmer1, 'event_name': event})
    swimmer2_entry = collection.find_one({'name': swimmer2, 'event_name': event})

    if swimmer1_entry is None or swimmer2_entry is None:
        # Return failure
        return jsonify({'success': False, 'message': 'Swimmer or event not found'})

    # Swap the ranking and points values
    result1 = collection.update_one({'name': swimmer1, 'event_name': event}, {'$set': {
                                    'ranking': swimmer2_entry['ranking'], 'points': swimmer2_entry['points']}})
    result2 = collection.update_one({'name': swimmer2, 'event_name': event}, {'$set': {
                                    'ranking': swimmer1_entry['ranking'], 'points': swimmer1_entry['points']}})

    if result1.matched_count == 1 and result1.modified_count == 1 and result2.matched_count == 1 and result2.modified_count == 1:
        # Return success
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Error updating database'})



@app.route('/results')
def display_results():
    # Get the results from the session
    results = session.get('results', [])

    # Render the results template with the results list
    return render_template('results.html', results=results)
