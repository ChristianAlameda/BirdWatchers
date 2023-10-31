#pip install flask 
from flask import Flask, render_template, request, jsonify
from database import Database
import requests
#pip install requests


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
        
        #VIEWING
        self.app.add_url_rule('/view', 'view', self.view)
        
        
        #CLASS INITIALIZATION
        self.database = Database()
        self.database.connect()

    def index(self):
        return render_template('home.html')

    def add(self):
        common_names_list = ['Sparrow', 'Eagle', 'Robin', 'Hawk', 'Crow', 'Pigeon', 'Owl', 'Pelican', 'Penguin', 'Parrot', 'Hummingbird', 'Woodpecker', 'Duck', 'Goose', 'Swallow', 'Seagull', 'Finch', 'Jay', 'Cardinal', 'Bluebird', 'Vulture', 'Kingfisher', 'Heron', 'Albatross', 'Flamingo', 'Kiwi', 'Falcon', 'Peacock', 'Toucan', 'Chickadee']
        genus_names_list = ['Sparrow - Genus: Passer', 'Eagle - Genus: Aquila', 'Robin - Genus: Turdus', 'Hawk - Genus: Buteo', 'Crow - Genus: Corvus', 'Pigeon - Genus: Columba', 'Owl - Genus: Strix (for some species)', 'Pelican - Genus: Pelecanus', 'Penguin - Genus: Spheniscus (for some species)', 'Parrot - Genus: Psittacus (for some species)', 'Hummingbird - Genus: Archilochus (for some species)', 'Woodpecker - Genus: Picoides (for some species)', 'Duck - Genus: Anas', 'Goose - Genus: Anser (for some species)', 'Swallow - Genus: Hirundo', 'Seagull - Genus: Larus (for some species)', 'Finch - Genus: Fringilla (for some species)', 'Jay - Genus: Cyanocitta', 'Cardinal - Genus: Cardinalis', 'Bluebird - Genus: Sialia', 'Vulture - Genus: Cathartes (for some species)', 'Kingfisher - Genus: Alcedo (for some species)', 'Heron - Genus: Ardea', 'Albatross - Genus: Diomedea', 'Flamingo - Genus: Phoenicopterus', 'Kiwi - Genus: Apteryx', 'Falcon - Genus: Falco', 'Peacock - Genus: Pavo', 'Toucan - Genus: Ramphastos']
        species_names_list = ['Sparrow (Genus: Passer) - House Sparrow (Passer domesticus)', 'Eagle (Genus: Aquila) - Golden Eagle (Aquila chrysaetos)', 'Robin (Genus: Turdus) - American Robin (Turdus migratorius)', 'Hawk (Genus: Buteo) - Red-tailed Hawk (Buteo jamaicensis)', 'Crow (Genus: Corvus) - American Crow (Corvus brachyrhynchos)', 'Pigeon (Genus: Columba) - Rock Pigeon (Columba livia)', 'Owl (Genus: Strix) - Barred Owl (Strix varia)', 'Pelican (Genus: Pelecanus) - American White Pelican (Pelecanus erythrorhynchos)', 'Penguin (Genus: Spheniscus) - Humboldt Penguin (Spheniscus humboldti)', 'Parrot (Genus: Psittacus) - Psittacus erithacus (African Grey Parrot)', 'Hummingbird (Genus: Archilochus) - Ruby-throated Hummingbird (Archilochus colubris)', 'Woodpecker (Genus: Picoides) - Downy Woodpecker (Picoides pubescens)', 'Duck (Genus: Anas) - Mallard (Anas platyrhynchos)', 'Goose (Genus: Anser) - Greylag Goose (Anser anser)', 'Swallow (Genus: Hirundo) - Barn Swallow (Hirundo rustica)', 'Seagull (Genus: Larus) - Herring Gull (Larus argentatus)', 'Finch (Genus: Fringilla) - Common Chaffinch (Fringilla coelebs)', 'Jay (Genus: Cyanocitta) - Blue Jay (Cyanocitta cristata)', 'Cardinal (Genus: Cardinalis) - Northern Cardinal (Cardinalis cardinalis)', 'Bluebird (Genus: Sialia) - Eastern Bluebird (Sialia sialis)', 'Vulture (Genus: Cathartes) - Turkey Vulture (Cathartes aura)', 'Kingfisher (Genus: Alcedo) - Common Kingfisher (Alcedo atthis)', 'Heron (Genus: Ardea) - Great Blue Heron (Ardea herodias)', 'Albatross (Genus: Diomedea) - Wandering Albatross (Diomedea exulans)', 'Flamingo (Genus: Phoenicopterus) - Greater Flamingo (Phoenicopterus roseus)', 'Kiwi (Genus: Apteryx) - North Island Brown Kiwi (Apteryx mantelli)', 'Falcon (Genus: Falco) - Peregrine Falcon (Falco peregrinus)', 'Peacock (Genus: Pavo) - Indian Peafowl (Pavo cristatus)', 'Toucan (Genus: Ramphastos) - Keel-billed Toucan (Ramphastos sulfuratus)']
        native_regions_list = ['North America', 'South America', 'Euroupe', 'Africa', 'Asia', 'Australia', 'Antartica']
        climate_list = ['tropical','dry','temperate','continental','polar']
        country_list = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'The Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo, Democratic Republic of the', 'Congo, Republic of the', 'Costa Rica', 'CÃ´te dâ€™Ivoire', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor (Timor-Leste)', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'The Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea, North', 'Korea, South', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia, Federated States of', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar (Burma)', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Sudan, South', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
        diet_list = ['Carnivorous', 'Herbivorous', 'Omnivorous', 'Piscivorous', 'Scavengers', 'Filter', 'Specialized']
        beak_description_list = ['Sharp Beak', 'Conical Beak', 'Long, Probing Beak', 'Serrated Beak', 'Curved Beak', 'Chisel-Like Beak', 'Tube-Shaped Beak', 'Spoon-Shaped Beak', 'Crossed Beak', 'Hooked Beak']
        colors_list = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Pink', 'Brown', 'Black', 'White', 'Gray', 'Cyan', 'Magenta', 'Teal', 'Lavender', 'Maroon', 'Indigo', 'Turquoise', 'Gold', 'Silver']
        feather_type_list = ['Contour feathers', 'Down feathers', 'Semiplume feathers', 'Filoplume feathers', 'Bristle feathers', 'Aftershaft feathers', 'Flight feathers', 'Tail feathers', 'Coverts (wing and tail)', 'Tertiary feathers', 'Scapular feathers', 'Auricular feathers', 'Rictal bristles', 'Eyebrow feathers', 'Nuptial plumage', 'Brood patch feathers', 'Powder down feathers', 'Crest feathers', 'Hackles (neck feathers)', 'Speculum feathers (often found in ducks)']
        behavior_description_list = ['Migratory', 'Territorial', 'Cannibalistic', 'Nesting', 'Courtship', 'Parental', 'Aggressive', 'Flocking', 'Camouflaging', 'Tool Use']
        concern_list = ['Least Concern (LC)', 'Near Threatened (NT)', 'Vulnerable (VU)', 'Endangered (EN)', 'Critically Endangered (CR)', 'Extinct in the Wild (EW)', 'Extinct (EX)', 'Data Deficient (DD)', 'Not Evaluated (NE)']
        
        
        return render_template('add.html', common_names_list=common_names_list, genus_names_list=genus_names_list, species_names_list=species_names_list, native_regions_list=native_regions_list, climate_list=climate_list, country_list=country_list, diet_list=diet_list, beak_description_list=beak_description_list, colors_list=colors_list, feather_type_list=feather_type_list, behavior_description_list=behavior_description_list, concern_list=concern_list)

    def new_added_document(self):
        data = request.json  # Access the JSON data sent in the POST request

        # Process and store the data as needed
        # For demonstration, we'll simply print the data to the console
        print(data)
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
        
        
        
        
        
        # common_name = request.form['common_name']
        # genus_name = request.form['genus_name']
        # species_name = request.form['species_name']
        # native_region = request.form['native_region']
        # country = request.form['country']
        # climate = request.form['climate']
        # latitude = request.form['latitude']
        # longitude = request.form['longitude']
        # diet = request.form['diet']
        # avg_lifespan = request.form['avg_lifespan']
        # height = request.form['height']
        # weight = request.form['weight']
        # wingspan = request.form['wingspan']
        # beak_description = request.form['beak_description']
        # color = request.form['color']
        # feather_type = request.form['feather_type']
        # behavior_description = request.form['behavior_description']
        # concern = request.form['concern']
        # last_updated = request.form['last_updated']
        # insertion = {
        #     "names": {
        #         "common_name": common_name,
        #         "genus_name":genus_name,
        #         "species_name":species_name
        #     },
        #     "nat_habitat": {
        #         "native_regions": native_region,
        #         "known_locations": [
        #             {
        #                 "country":country,
        #                 "latitude":latitude,
        #                 "longitude":longitude
        #             },
        #             # Additional locations here
        #         ],
        #         "habitat_desc":climate
        #     },
        #     "diet":diet,  
        #     "avg_lifespan":avg_lifespan,  
        #     "phys_features": {
        #         "height":height,
        #         "weight":weight,
        #         "wingspan":wingspan,
        #         "beak_description":beak_description,
        #         "feather_type":feather_type,
        #         "color":color          
        #     },
        #     "behavior": {
        #         "behavior_description":behavior_description
        #     },
        #     "conservation_status": {
        #         "concern": concern,
        #         "last_updated":last_updated
        #     }
        # }
        
            
        return "YOU HAVE SUCCESSFULLY ADDED A DOCUMENT PRESS THIS LINK TO GET BACK TO THE HOMEPAGE <br><br><a href='../'>Visit Homepage</a>" 
    
    def rem(self):
        return render_template('rem.html', x="hello")
    
    def new_removed_document(self):
        return "YOU HAVE SUCCESSFULLY REMOVED A DOCUMENT PRESS THIS LINK TO GET BACK TO THE HOMEPAGE <br><br><a href='../'>Visit Homepage</a>" 

    def view(self):
        allPosts = self.databaseClass.getPosts({})
        return render_template('view.html', allPosts=allPosts)

if __name__ == "__main__":
    x = MyFlaskApp()
    x.app.run(host="0.0.0.0", port=7777)

# test comment