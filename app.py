#pip install flask 
#pip install requests
from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from database import Database
from userDatabase import UserDatabase
import bcrypt
import json
import re
from bson import ObjectId

class MyFlaskApp:
    def __init__(self):
        # GLOBAL VARS
        self.curr_email = ''
        self.selected_result = ''

        # Initialize Flask app
        self.app = Flask(__name__, static_url_path='/static')   # COLE - Added "static_url_path='/static" to reference static files in code
        self.app.secret_key = 'your_secret_key_here'

        ### APP ROUTES ###
        # AUTH PATHS
        self.app.add_url_rule('/logged_in', 'logged_in', self.logged_in)
        self.app.add_url_rule('/login', 'login', self.login, methods=['POST', 'GET'])
        self.app.add_url_rule('/logout', 'logout', self.logout, methods=['POST', 'GET'])
        self.app.add_url_rule('/', 'index', self.index, methods=['POST', 'GET'])
        # HOME
        self.app.add_url_rule('/home', 'home', self.home)   # NOTE: Changed to home from /
        # REMOVING
        self.app.add_url_rule('/rem', 'rem', self.rem)
        self.app.add_url_rule('/rem/new_removed_document', 'new_removed_document', self.new_removed_document, methods=['POST'])
        # IDENTIFYING & ADDING
        self.app.add_url_rule('/identify', 'identify', self.identify)
        self.app.add_url_rule('/identify/id_results', 'id_results', self.id_results, methods=['POST'])
        self.app.add_url_rule('/identify/id_results/add', 'add', self.add, methods=['POST'])
        self.app.add_url_rule('/identify/id_results/add/add_details', 'add_details', self.add_details, methods=['POST'])
        # VIEWING
        self.app.add_url_rule('/view', 'view', self.view)
        
        # DB CLASS INITIALIZATION
        self.database = Database()
        self.database.connect()
        self.database.checkIfEmpty()
        
        # AUTH DATABASE INITIALIZATION
        self.user_database = UserDatabase()
        self.user_database.connect('auth')
    
    ######################################
    ######################################
    ########### AUTHORIZATION ############
    ######################################
    ######################################


    def index(self):
        message = ''
        # if "email" in session:
        #     return redirect(url_for("logged_in"))
        if request.method == "POST":
            user = request.form.get("fullname")
            email = request.form.get("email")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            result = self.register_user(user, email, password1, password2)
            
            if result == email:
                self.curr_email = email
                return render_template('auth/logged_in.html', email=result)
            else:
                message = result
                return render_template('auth/index.html', message=message)
        return render_template('auth/index.html')
    
    def login(self):
        message = 'Please login to your account'
        # if "email" in session:
        #     return redirect(url_for("logged_in"))

        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            email_found = self.user_database.find_user_by_email(email)
            if email_found:
                email_val = email_found['email']
                passwordcheck = email_found['password']

                if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                    session["email"] = email_val
                    self.curr_email = email_val
                    return redirect(url_for('home'))#MAY CHANGE logged_in
                else:
                    if "email" in session:
                        return redirect(url_for("home"))#MAY CHANGE
                    message = 'Wrong password'
                    return render_template('auth/login.html', message=message)
            else:
                message = 'Email not found'
                return render_template('auth/login.html', message=message)
        return render_template('auth/login.html', message=message)

    def logged_in(self):
        if "email" in session:
            email = session["email"]
            self.curr_email = email
            return render_template('home.html', email=email)#changed from auth/logged_in.html
        else:
            return redirect(url_for("login"))
        
    def register_user(self, user, email, password1, password2):
        
        user_found = self.user_database.find_user_by_name(user)
        email_found = self.user_database.find_user_by_email(email)
        
        
        if user_found:
            return 'There already is a user by that name'
        if email_found:
            return 'This email already exists in the database'
        if password1 != password2:
            return 'Passwords should match'

        hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
        user_input = {'name': user, 'email': email, 'password': hashed}
        self.user_database.insert_user(user_input)
        user_data = self.user_database.find_user_by_email(email)
        new_email = user_data['email']
        return new_email
    
    #NOT REALLY USING THIS
    def logout(self):
        if "email" in session:
            session.pop("email", None)
            return render_template("auth/signout.html")
        else:
            return redirect(url_for('index'))
    
    ######################################
    ######################################
    ############# ACTUAL APP #############
    ######################################
    ######################################
    
    def home(self):
        return render_template('home.html', email=self.curr_email)

    def rem(self):
        self.user_database.connect(self.curr_email)
        all_posts = self.user_database.getPosts({})
        # print(all_posts[0])
        #all_posts_list = []
        #for i in all_posts:
        #    all_posts_list.append(i)

        all_posts_list = list(all_posts)
            
        if all_posts == None:
            message = "You do not currently have any items in your collection yet please go back to the homeapge<br><br><a href='home'>Visit Homepage</a>"
            return message
        else:
            return render_template('rem.html', all_posts=all_posts_list)
    
    def new_removed_document(self):
        self.user_database.connect(self.curr_email)
        posts = request.form.getlist('document')
        print(posts)
        if len(posts) == 1:
            self.user_database.deletePost({'_id':ObjectId(posts[0])})
            return "YOU HAVE SUCCESSFULLY REMOVED A DOCUMENT PRESS THIS LINK TO GET BACK TO THE HOMEPAGE <br><br><a href='home'>Visit Homepage</a>" 
        if len(posts) == 0:
            return "YOU HAVE NO ITEMS IN THE LIST PLEASE RETURN TO HOMEPAGE<br><br><a href='home'>Visit Homepage</a>" 
        else:
            for i in posts:
                self.user_database.deletePosts({'_id':ObjectId(posts[i])})
            return "YOU HAVE SUCCESSFULLY REMOVED SEVERAL DOCUMENTS PRESS THIS LINK TO GET BACK TO THE HOMEPAGE <br><br><a href='home'>Visit Homepage</a>" 
    
    def identify(self):
        active        = ['Morning','Noon','Afternoon','Evening']
        beak_type     = ['Filtering', 'Probing', 'Catching Insects', 'Cracking Seeds', 'Tearing Meat', 'Drilling']
        feather_color = ['Black', 'White', 'Gray', 'Brown', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Violet']

        return render_template('identify.html', active=active, feather_color=feather_color, beak_type=beak_type)
    
    def id_results(self):
        # For debugging purposes
        log_title = "[Method: id_results()]:\n"
        print(log_title, "Method START\n")
        print("")

        # Retrieve user-selected values from HTML forms
        active = request.form.get('active')
        feather_color = request.form.getlist('feather_color')
        beak_type = request.form.get('beak_type')
        bird_size = request.form.get('bird_size')

        print(log_title, "Value of active: ", active)
        print(log_title, "Value of feather_color: ", feather_color)
        print(log_title, "Value of beak_type: ", beak_type)
        print(log_title, "Value of bird_size: ", bird_size)

        #bird_size_mapping = {
        #    "xsmall": {"min_height": 0, "max_height": 3.9, ""},
        #    "small":  {"min": 4, "max": 7},
        #    "medium": {"min": 7.1, "max": 13},
        #    "large":  {"min": 13.1, "max": 19.9},
        #    "xlarge": {"min": 20, "max": float('inf')}
        #}

        bird_size_mapping = {
            "xsmall": {"height_min": 0, "height_max": 7.9},
            "small": {"height_min": 7.9, "height_max": 11},
            "medium": {"height_min": 11, "height_max": 16},
            "large": {"height_min": 16, "height_max": 30},
            "xlarge": {"height_min": 30, "height_max": float('inf')}
        }

        # ERROR FIX: Initialize size_range even if bird_size is NULL --> avoids attempting to access size_range before it's defined
        if bird_size is None:
            size_range = {"min": 0, "max": float('inf')}
        else:
            size_range = bird_size_mapping[bird_size]

        # Convert time of day to corresponding value in DB
        if active in ['Morning', 'Noon', 'Afternoon']:
            active = 'Diurnal'
        elif active == 'Evening':
            active = 'Nocturnal'

        # Construct query dict to be passed to DB
        query = {
            "active": active,
            "phys_features.feather_color": {"$all": feather_color},
            "phys_features.beak_type": beak_type,
            "phys_features.height": {"$gte": size_range['height_min'], "$lte": size_range['height_max']}
        }
        
        print(log_title, "Connecting to database...")
        self.database.connect()
        print(log_title, "Connected.")

        # Perform query and store results in results
        print(log_title, "Performing query...")
        results = self.database.getPosts(query)
        print("")
        print(log_title, "Raw query results data: ", results)
        print("")

        # Check if results are empty [] --> have to convert cursor that's returned from DB to list, check_empty() handles this.
        print(log_title, "Checking if query results are empty...")
        results_list, is_empty = self.check_empty(results)

        # If results empty --> render /identify page with no results message
        if is_empty:
            print(log_title, "No results: True")
            return render_template('identify.html', no_results=True)

        # Iterate through results_list and create array containing each retrieved document
        items = [result for result in results_list]
        print("")
        print(log_title, "Final items: ", "   ", type(items), "   ", items)
        print("")

        print(log_title, "Method END.")
        print("")

        return render_template('results.html', query_results=items)
    
    def add(self):
        # For debugging purposes
        log_title = "[Method: add()]:\n"
        print(log_title, "Method START.")

        # Retrieve selected (single) item from query results => retrieved from user selection on 'results.html' page
        self.selected_result = request.form.get('selected_item')
        print(log_title, "Selected query result retrieved.")

        # Parsing selected query result str to dict
        self.selected_result = self.parseStringToDict(self.selected_result)
        print(log_title, "Selected query result string parsed to dict.")
        print(log_title, "Printing dict below...")
        print("")
        print(type(self.selected_result), self.selected_result)
        print("")

        # Initialize to-be-added keys/fields for add_details()
        self.selected_result["sighting_summary"] = ""
        self.selected_result["sighting_date"] = ""

        print(log_title, "printing dict with new fields (currently empty): ", self.selected_result)
        print("")

        print(log_title, "Method END.")
        print("")

        return render_template('add_details.html', item=self.selected_result)

    def add_details(self):
        # For debugging purposes
        log_title = "[Method: add_details()]: "
        print(log_title, "Method START.")
        print("")

        # Define 'item' with current value of global var 'self.selected_result'
        item = self.selected_result

        # Retrieve user defined summary and date from 'add_details.html' page
        sighting_summary = request.form.get('sighting_summary')
        sighting_date = request.form.get('sighting_date')
        print("")
        print(log_title, "Current dict: ", item)
        print("")
        print(log_title, "Received summary value: ", sighting_summary)
        print(log_title, "Received date value: ", sighting_date)
        print("")

        # Insert retrieved summary and date values into current dict
        item["sighting_summary"] = sighting_summary
        item["sighting_date"] = sighting_date

        # Insert into user DB
        print(log_title, "ATTEMPTING TO INSERT INTO USER DATABASE...")
        print(log_title, "Connecting to user DB...")
        self.user_database.connect(self.curr_email)
        print(log_title, "Connected.")
        print(log_title, "Checking for dupes in user's collection...")
        item = self.catch_duplicate({"item":item})
        print(log_title, "No duplicates found.")
        print("")
        print(log_title, "Final item before insertion:",'  ',type(item), '  ', item)
        print("")
        print(log_title, "INSERTING...")
        self.user_database.insertPost(item)
        print(log_title, "Item has been successfully inserted into user's collection.")
        print(log_title, "Function END.")
        print("")

        return render_template('add_success.html')
        
    def view(self):
        # For debugging purposes
        log_title = "[Method: view()]:\n"
        print(log_title, "Method START.")
        print("")

        print(log_title, "Connecting to user DB...")
        self.user_database.connect(self.curr_email)
        print(log_title, "Connected.")

        # Retrieve all user's inserted documents
        print(log_title, "Retrieving user documents in collection...")
        all_posts = self.user_database.getPosts({})
        print(log_title, "Documents retrieved.")
        print("")

        # Convert cursor object to list
        all_posts_list = list(all_posts)
        print(log_title, "Printing documents below:\n", all_posts_list)
        print("")
            
        if all_posts == None:
            message = "You do not currently have any items in your collection yet please go back to the homeapge<br><br><a href='home'>Visit Homepage</a>"
            return message
        else:
            return render_template('view.html', all_posts=all_posts_list, email=self.curr_email)

    #################################
    #################################
    ######## HELPER FUCTIONS ########
    #################################
    #################################
    
    def parseStringToDict(self, stringedDictionary:str):
        # Define a regular expression pattern to match key-value pairs
        pattern = r"'(\w+)': (?:'([^']*)'|(?:\[(.*?)\])|(\d+\.\d+)|ObjectId\('([^']*)'\))"

        # Find all key-value pairs in the string
        matches = re.findall(pattern, stringedDictionary)

        # Create a dictionary from the matches
        data = {}
        for key, value_str, list_str, float_str, obj_id in matches:
            value = value_str if value_str else (list_str.split(', ') if list_str else (float(float_str) if float_str else obj_id))
            data[key] = value
        
        # data = self.remove_double_quotes(data)
        return data
    
    def catch_duplicate(self, item:dict):
        # see if a user has added a bird that 
        # he has already added
        #gives me a string
        print("item['item']",'  ',type(item['item']), '  ', item['item'])
        
        self.user_database.connect(self.curr_email)
        #remove the newest duplicate
        posts = self.user_database.getPost({'item':item})   # COLE - Changed original getPosts() method call to getPost() since only single query result is selected for adding to catalogue
        print(posts)
        # cursor_list = list(posts)
        # print(cursor_list)
        if posts:
            self.user_database.deletePost(posts)
            return False
        else: return item
    
    def check_empty(self, results):
        results_list = list(results)
        return results_list, len(results_list) == 0
        
    # def remove_double_quotes(self, item):
    #     if isinstance(item, list):
    #         return [self.remove_double_quotes(element) for element in item]
    #     elif isinstance(item, dict):
    #         return {key: self.remove_double_quotes(value) for key, value in item.items()}
    #     elif isinstance(item, str):
    #         return item.replace('"', '').replace("'", '')  # Remove both double and single quotes
    #     else:
    #         return item
        
if __name__ == "__main__":
    x = MyFlaskApp()
    x.app.run(host="0.0.0.0", port=7777)
