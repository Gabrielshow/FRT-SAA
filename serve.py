from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
import subprocess
import os
import json
from flask_cors import CORS
import tkinter as tk
from FRT import SeatAssignmentApp
import numpy as np
import cv2
from multiprocessing import Value
# from model import model

app = Flask(__name__)
CORS(app)

counter = Value('i', 0)
def save_img(img):
	with counter.get_lock():
		counter.value += 1
		count = counter.value
	img_dir = "esp32_imgs"
	if not os.path.isdir(img_dir):
		os.mkdir(img_dir)
	cv2.imwrite(os.path.join(img_dir,"img_"+str(count)+".jpg"), img)
	# print("Image Saved", end="\n") # debug
 
# Serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST','GET'])
def upload():
	received = request
	img = None
	if received.files:
		print(received.files['imageFile'])
		# convert string of image data to uint8
		file  = received.files['imageFile']
		nparr = np.fromstring(file.read(), np.uint8)
		# decode image
		img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		save_img(img)
		
		return "[SUCCESS] Image Received", 201
	else:
		return "[FAILED] Image Not Received", 204



@app.route('/get_grid_data', methods=['POST'])
def get_grid_data():
    data = request.get_json()
    selected_hall = data.get('selected_hall')
    selected_pattern = data.get('selected_pattern')
    grid_data = get_grid_data_json(selected_hall, selected_pattern)
    
    return jsonify(grid_data)

@app.route('/exam_hall')
def exam_hall():
    # Render the exam_hall.html template
    return render_template('exam_hall.html')

@app.route('/run_saa', methods=['POST'])
def run_saa():
    data = request.form
    # print(data)
    selected_hall = data.get('selected_hall')
    selected_pattern = data.get('selected_pattern')

    if not selected_hall or not selected_pattern:
        return jsonify({'error': 'Invalid selection'}), 400
    
    subprocess.run(["python", "FRT.py", selected_hall, selected_pattern])
    grid_data = get_grid_data_json(selected_hall, selected_pattern)
    print(grid_data)
    return render_template('exam_hall.html', seating_data=grid_data)

def get_grid_data_json(selected_hall, selected_pattern):
    root = tk.Tk()
    app = SeatAssignmentApp(root)
    return json.loads(app.get_grid_data_json(selected_hall, selected_pattern))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
