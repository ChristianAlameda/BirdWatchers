# use website: https://www.mongodb.com/try/download/community
# download mongodb version 7.0
from bird import x
import pymongo
class Database:
    def __init__(self):
        self.myclient = False
        self.mydb = False
        self.mycol = False
    
    def connect(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["BirdWatchers_Test"]
        self.mycol = self.mydb["BW_Test"]
        
    def insertPost(self, post:dict):
        self.mycol.insert_one(post).inserted_id
        
    def insertPosts(self, post):
        self.mycol.insert_many(post).inserted_ids
        
    def getPost(self, query:dict):
        return self.mycol.find_one(query)
    
    def getPosts(self, query:dict):
        return self.mycol.find(query)
    
    def printPosts(self):
        for post in self.mycol.find():
            print.pprint(post)

    def returnPosts(self):
        for post in self.mycol.find():
            yield post

    def deletePost(self, query:dict):
        self.mycol.delete_one(query)
    
    #collection.delete_many(filter, collation=None, 
    # hint=None, session=None)
    
    def deletePosts(self,query:dict):
        self.mycol.delete_many(query)
        
    def checkIfEmpty(self):
        data = self.getPosts({})
        if data:
            pass
        else: 
            self.inputAllData()
    
    def inputAllData(self):
        print(x)
        for bird in x: 
            self.insertPost(bird)
        
         
        
