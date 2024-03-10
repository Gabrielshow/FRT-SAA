import requests

# Replace 'http://localhost:5000/api/grid-data/<hall>/<pattern>' with the actual URL of your Flask endpoint
url = 'http://localhost:5000/run_saa'

# Send a GET request to the Flask application
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    print(response.content)
    data = response.json()
    
    # Print the JSON data
    print(data)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
