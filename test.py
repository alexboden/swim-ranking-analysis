from flask import Flask, render_template, request, session
from Meet.meet import Meet
from pypdf import PdfReader
from pymongo import MongoClient
from json import dumps as json_dump

client = MongoClient('mongodb://localhost:27017/')
db = client['swimdatabase']
collection = db['entries']


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('home.html', error='No file selected.')

        file_submission = request.files['file']

        # Check if the file is a PDF
        if file_submission.filename.split('.')[-1].lower() != 'pdf':
            return render_template('home.html', error='File must be a PDF.')


        # Process the PDF and display the results
        # This is where you would put your existing code to process the PDF
        # and generate the results
        # File to analyze
        reader = PdfReader(file_submission.filename)
        text_extract = ""

        for i in range(len(reader.pages)):
            text_extract += (reader.pages[i].extract_text())

        m = Meet(text_extract)
        e = m.events[0]
        collection.delete_many({})
        
        for event in m.events:
            for entry in event.entries:
                collection.insert_one(entry.__dict__)
        results = m.get_team_breakdown("Men")
        entries = db['entries'].find()

        entries_by_event = {}
        
        for entry in entries:
            entries_by_event[entry['event_name']] = entries_by_event.get(entry['event_name'], []) + [entry]
        
        return render_template('broken_out_by_entry.html', events=entries_by_event)
        # Render the template and pass the entries as a parameter
        return render_template('entries.html', entries=entries)
        return render_template('individual_results.html', event=e)

    # If the request method is GET, render the home page
    return render_template('home.html')

# Define the route for displaying the results


@app.route('/results')
def display_results():
    # Get the results from the session
    results = session.get('results', [])

    # Render the results template with the results list
    return render_template('results.html', results=results)
