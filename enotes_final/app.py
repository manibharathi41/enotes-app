import os
import json
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# --- CONFIGURATION ---
# This ensures it works on both your laptop and the free cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
DB_FILE = os.path.join(BASE_DIR, 'notes.json')

@app.route('/')
def index():
    # 1. Get the Search Query (if any)
    query = request.args.get('q', '').lower()
    
    # 2. Load Data from JSON file
    with open(DB_FILE, 'r') as f:
        all_notes = json.load(f)
    
    # 3. Filter results if searching
    if query:
        notes = []
        for note in all_notes:
            # Search by Code (GE3451) or Title (Maths)
            if query in note['code'].lower() or query in note['title'].lower():
                notes.append(note)
    else:
        notes = all_notes

    return render_template('index.html', notes=notes, query=query)

# Route for "View" (Opens in Browser)
@app.route('/view/<filename>')
def view_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Route for "Download" (Forces Download)
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)