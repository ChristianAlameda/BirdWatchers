#pip install flask 
from flask import Flask, render_template, request, jsonify
from database import Database
from list_creator import common_name
from list_creator import genus_name
from list_creator import species_name
from list_creator import climate
from list_creator import country
from list_creator import diet
from list_creator import beak_description
from list_creator import color
from list_creator import feather_type
from list_creator import behavior_description
from list_creator import concern

#pip install requests
import requests
import json



class MyFlaskApp:
    def __init__(self):
        # Initialize Flask app
        self.app = Flask(__name__)

        # Connect to the database
        self.databaseClass = Database()
        self.databaseClass.connect()

        # Add routes to the app
        self.app.add_url_rule('/', 'index', self.index)
        #ADDING
        self.app.add_url_rule('/add', 'add', self.add)
        self.app.add_url_rule('/add/new_added_document', 'new_added_document', self.new_added_document, methods=['POST'])
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

    def index(self):
        return render_template('home.html')

    def add(self):
        return render_template('add.html', common_names_list=common_name, genus_names_list=genus_name, species_names_list=species_name, climate_list=climate, country_list=country, diet_list=diet, beak_description_list=beak_description, colors_list=color, feather_type_list=feather_type, behavior_description_list=behavior_description, concern_list=concern)

    def new_added_document(self):
        data = request.json  # Access the JSON data sent in the POST request

        # Process and store the data as needed
        #iterate throught the forms
        for i in data: 
            common_name =i['common_name'] 
            genus_name =i['genus_name'] 
            species_name =i['species_name'] 
            native_region =i['native_region'] 
            country =i['country'] 
            climate =i['climate'] 
            latitude =i['latitude'] 
            longitude =i['longitude'] 
            diet =i['diet'] 
            avg_lifespan =i['avg_lifespan'] 
            height =i['height'] 
            weight =i['weight'] 
            wingspan =i['wingspan'] 
            beak_description =i['beak_description'] 
            color = i['color'] 
            feather_type =i['feather_type'] 
            behavior_description = i['behavior_description'] 
            concern =i['concern'] 
            last_updated =i['last_updated'] 
            
            insertion = {
                "names": {
                    "common_name": common_name,
                    "genus_name":genus_name,
                    "species_name":species_name
                },
                "nat_habitat": {
                    "native_regions": native_region,
                    "known_locations": [
                        {
                            "country":country,
                            "latitude":latitude,
                            "longitude":longitude
                        },
                        # Additional locations here
                    ],
                    "habitat_desc":climate
                },
                "diet":diet,  
                "avg_lifespan":avg_lifespan,  
                "phys_features": {
                    "height":height,
                    "weight":weight,
                    "wingspan":wingspan,
                    "beak_description":beak_description,
                    "feather_type":feather_type,
                    "color":color          
                },
                "behavior": {
                    "behavior_description":behavior_description
                },
                "conservation_status": {
                    "concern": concern,
                    "last_updated":last_updated
                }
            }
            self.database.insertPost(insertion)
            print('entry entered')

        return "YOU HAVE SUCCESSFULLY ADDED A DOCUMENT PRESS THIS LINK TO GET BACK TO THE HOMEPAGE <br><br><a href='../'>Visit Homepage</a>" 
    
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
        
        # Perform query and store results in results
        results = self.database.getPosts(query)

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

        return json_results

    def view(self):
        return render_template('view.html', all_posts=self.database.getPosts({}))

if __name__ == "__main__":
    x = MyFlaskApp()
    x.app.run(host="0.0.0.0", port=7777)

# test comment