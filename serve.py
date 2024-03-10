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

# @app.route('/api/grid-data/<hall>/<pattern>')
# def get_grid_data(hall, pattern):
#     # Initialize the SeatAssignmentApp with the selected hall and pattern
#     root = tk.Tk()
#     app = FRT.SeatAssignmentApp(root)
#     app.update_seat_grid(hall, pattern)
    
#     # Get the grid data
#     grid_data = app.get_grid_data(app.seat_grid)
    
#     # Return the grid data as JSON
#     return jsonify(grid_data)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/run_saa', methods=['POST'])
# def run_saa():
#     data = request.form # Assuming form data is sent
#     selected_hall = data.get('selected_hall')
#     selected_pattern = data.get('selected_pattern')

#     # Validating user input
#     if not selected_hall or not selected_pattern:
#         return jsonify({'error': 'Invalid selection'}), 400

#     # Initialize the SeatAssignmentApp with the selected hall and pattern
#     root = tk.Tk()
#     app = FRT.SeatAssignmentApp(root)
#     app.update_seat_grid(selected_hall, selected_pattern)
    
#     # Get the grid data
#     grid_data = app.get_grid_data(app.seat_grid)
    
#     # Return the grid data as JSON
#     return jsonify(grid_data)



@app.route('/run_saa', methods=['POST'])
def run_saa():
    data = request.form # Assuming form data is sent
    selected_hall = data.get('selected_hall')
    selected_pattern = data.get('selected_pattern')

    # Validating user input
    if not selected_hall or not selected_pattern:
        return jsonify({'error': 'Invalid selection'}), 400
    subprocess.run(["python", "FRT.py", selected_hall, selected_pattern])
    root = tk.Tk()
    app = SeatAssignmentApp(root)
    # Calling saa.py with the selected parameters
    grid_data_json = app.get_grid_data_json(selected_hall, selected_pattern)    
    return jsonify(json.loads(grid_data_json))

if __name__ == '__main__':
    app.run(debug=True)
