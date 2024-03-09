from flask import Flask, render_template, request, jsonify
import Saa  # Import your Saa.py script

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_saa', methods=['POST'])
def run_saa():
    data = request.json  # Assuming JSON data is sent in the request
    
    # Extract user input from the request data
    selected_hall = data.get('selected_hall')
    selected_pattern = data.get('selected_pattern')

    # Validate user input
    if selected_hall not in ['TLT', 'FLT'] or selected_pattern not in ['Checkerboard', 'Zigzag']:
        return jsonify({'error': 'Invalid selection'}), 400

    # Run Saa.py with user input
    result = Saa.run_saa(selected_hall, selected_pattern)

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
