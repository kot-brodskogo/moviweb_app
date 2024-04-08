from flask import Flask
from datamanager.json_data_manager import JSONDataManager
import os

# Define the path to the data.json file
data_json_path = os.path.join(os.path.dirname(__file__), 'datamanager', 'data.json')

app = Flask(__name__)
data_manager = JSONDataManager(data_json_path)  # Use the appropriate path to your JSON file


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)  # Temporarily returning users as a string


if __name__ == '__main__':
    app.run(debug=True)
