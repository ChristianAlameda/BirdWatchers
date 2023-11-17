from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add')
def add():
    return render_template('som.html')

@app.route('/add/new_added_document', methods=['POST'])
def add1():
    data = request.json  # Access the JSON data sent in the POST request

    # Process and store the data as needed
    # For demonstration, we'll simply print the data to the console
    print(data)

    return jsonify({'message': 'Data received successfully'})

if __name__ == '__main__':
    app.run()
