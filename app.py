#pip install flask 
from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from database import Database
from userDatabase import UserDatabase
import bcrypt

#pip install requests
import json



class MyFlaskApp:
    def __init__(self):
        self.curr_email = ''
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.secret_key = 'your_secret_key_here'
        #AUTH PATHS
        self.app.add_url_rule('/logged_in', 'logged_in', self.logged_in)
        self.app.add_url_rule('/login', 'login', self.login, methods=['POST', 'GET'])
        self.app.add_url_rule('/logout', 'logout', self.logout, methods=['POST', 'GET'])
        self.app.add_url_rule('/', 'index', self.index, methods=['POST', 'GET'])
        
        
        

        # Add routes to the app
        #Changed to home from /
        self.app.add_url_rule('/home', 'home', self.home)
        # #ADDING
        self.app.add_url_rule('/add', 'add', self.add, methods=['POST'])
        #REMOVING
        self.app.add_url_rule('/rem', 'rem', self.rem)
        self.app.add_url_rule('/rem/new_removed_document', 'new_removed_document', self.new_removed_document, methods=['POST'])
        #IDENTIFYING
        self.app.add_url_rule('/identify', 'identify', self.identify)
        self.app.add_url_rule('/identify/id_submission', 'id_submission', self.id_submission, methods=['POST'])
        
        #VIEWING
        self.app.add_url_rule('/view', 'view', self.view)
        
        
        #CLASS INITIALIZATION
        self.database = Database()
        self.database.connect()
        
        #AUTH DATABASE
        self.user_database = UserDatabase()
        self.user_database.connect('auth')
    
    ######################################
    ######################################
    ########### AUTHORIZATION ############
    ######################################
    ######################################


    def index(self):
        message = ''
        if "email" in session:
            return redirect(url_for("logged_in"))
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
        if "email" in session:
            return redirect(url_for("logged_in"))

        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            email_found = self.user_database.find_user_by_email(email)
            if email_found:
                email_val = email_found['email']
                passwordcheck = email_found['password']

                if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                    print('hello')
                    session["email"] = email_val
                    self.curr_email = email_val
                    return redirect(url_for('logged_in'))#MAY CHANGE
                else:
                    if "email" in session:
                        return redirect(url_for("logged_in"))#MAY CHANGE
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
        return render_template('home.html')

    def rem(self):
        return render_template('rem.html', all_posts=self.database.getPosts({}))
    
    def new_removed_document(self):
        return "YOU HAVE SUCCESSFULLY REMOVED A DOCUMENT PRESS THIS LINK TO GET BACK TO THE HOMEPAGE <br><br><a href='../'>Visit Homepage</a>" 
    
    def identify(self):
        active        = ['Morning','Noon','Afternoon','Evening']
        beak_type     = ['Filtering', 'Probing', 'Catching Insects', 'Cracking Seeds', 'Tearing Meat', 'Drilling']
        feather_color = ['Black', 'White', 'Gray', 'Brown', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Violet']

        return render_template('identify.html', active=active, feather_color=feather_color, beak_type=beak_type)
    
    def id_submission(self):
        # Grab user-selected values from HTML forms
        active = request.form.get('active')
        feather_color = request.form.getlist('feather_color')
        beak_type = request.form.get('beak_type')

        # Convert time of day to corresponding value in DB
        if active in ['Morning', 'Noon', 'Afternoon']:
            active = 'Diurnal'
        elif active == 'Evening':
            active = 'Nocturnal'

        # Construct query object
        query = {
            "phys_features.plumage_color": {"$in": feather_color},
            "phys_features.beak_type": beak_type,
            "active": active
        }
        
        self.database.connect()
        # Perform query and store results in results
        print(self.database.getPosts(query))
        results = list(self.database.getPosts(query))


        results_list = [doc for doc in results]

        for result in results_list:
            result['_id'] = str(result['_id'])

        json_results = json.dumps(results_list)

        # Print to console for debugging
        print("Active:", active)
        print("Feather Color:", feather_color)
        print("Beak Type:", beak_type)
        print("Query:", query)
        print("Results:", json_results)

        return render_template('add.html',json_results=json_results)

    def add(self):
        item = request.form.get("selected_items")
        self.user_database.connect(self.curr_email)
        self.user_database.insertPost({"item":item})
        
    def view(self):
        return render_template('view.html', all_posts=self.database.getPosts({}))

if __name__ == "__main__":
    x = MyFlaskApp()
    x.app.run(host="0.0.0.0", port=7777)

# test comment