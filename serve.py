from flask import Flask, request, jsonify, render_template, send_from_directory
import FRT
import subprocess

app = Flask(__name__)

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
    data = request.form # Assuming form data is sent
    selected_hall = data.get('selected_hall')
    selected_pattern = data.get('selected_pattern')

    # Validate user input
    if not selected_hall or not selected_pattern:
        return jsonify({'error': 'Invalid selection'}), 400

    # Call saa.py with the selected parameters
    subprocess.run(["python", "FRT.py", selected_hall, selected_pattern])

    return jsonify({'result': 'Success'})

if __name__ == '__main__':
    app.run(debug=True)
