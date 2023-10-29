from flask import Flask, render_template
from database import Database

class MyFlaskApp:
    def __init__(self):
        # Initialize Flask app
        self.app = Flask(__name__)

        # Connect to the database
        self.databaseClass = Database()
        self.databaseClass.connect()

        # Add routes to the app
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/add', 'add', self.add)
        self.app.add_url_rule('/rem', 'rem', self.rem)
        self.app.add_url_rule('/view', 'view', self.view)

    def index(self):
        return render_template('home.html')

    def add(self):
        return render_template('add.html')

    def rem(self):
        return render_template('rem.html')

    def view(self):
        allPosts = self.databaseClass.getPosts({})
        return render_template('view.html', allPosts=allPosts)

if __name__ == "__main__":
    x = MyFlaskApp()
    x.app.run(host="0.0.0.0", port=7777)