import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# Load database from local file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'notes.json')

@app.route('/')
def index():
    query = request.args.get('q', '').lower()
    
    with open(DB_FILE, 'r') as f:
        all_notes = json.load(f)
    
    if query:
        notes = []
        for note in all_notes:
            if query in note['code'].lower() or query in note['title'].lower():
                notes.append(note)
    else:
        notes = all_notes

    return render_template('index.html', notes=notes, query=query)

if __name__ == '__main__':
    app.run(debug=True)
