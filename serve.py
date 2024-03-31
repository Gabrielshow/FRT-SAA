from flask import Flask, request, jsonify, render_template, send_from_directory
import subprocess
import os
import json
from flask_cors import CORS
import tkinter as tk
from FRT import SeatAssignmentApp

app = Flask(__name__)
CORS(app)

# Serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_saa', methods=['POST'])
def run_saa():
    data = request.form
    selected_hall = data.get('selected_hall')
    selected_pattern = data.get('selected_pattern')

    if not selected_hall or not selected_pattern:
        return jsonify({'error': 'Invalid selection'}), 400
    
    subprocess.run(["python", "FRT.py", selected_hall, selected_pattern])
    root = tk.Tk()
    app = SeatAssignmentApp(root)
    grid_data = app.get_grid_data(app.seat_grid_instance.seat_grid)  # Get the grid data directly

    # Render the exam hall template and pass the grid data to it
    return render_template('exam_hall.html', seating_data=grid_data)

if __name__ == '__main__':
    app.run(debug=True)
