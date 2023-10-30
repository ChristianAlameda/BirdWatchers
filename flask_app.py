import random

from flask import Flask, request, render_template
from pymongo import MongoClient
import pymongo


app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['Avilog_ALPHA']
collection = db['users']

html_form = """<!DOCTYPE html>
<html>
<head>
    <title>User Registration Form</title>
</head>
<body>
    <h1>User Registration Form</h1>
    <form name="registrationForm" action="/submit" method="post">
    
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br>

        <!-- Add more input fields for other data -->
        
        <input type="submit" value="Submit">
        <input type="reset" value="Reset">
    </form>
</body>


</html>"""

@app.route('/registration', methods=['GET'])
def show_registration_form():
    return html_form

@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        #_id = generate_user_id()
        
        # Insert the data into MongoDB
        user_data = {
            #"_id": _id,
            "username": username,
            "email": email
        }
        collection.insert_one(user_data)
        #collection.create_index([("user_id", pymongo.ASCENDING)], unique=True)

        return "Data submitted successfully."


def generate_user_id():
    while True:
        user_id = f'BW{random.randint(1, 99999999):08}'
        return user_id

if __name__ == '__main__':
    app.run(debug=True)
