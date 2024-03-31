from pymongo import MongoClient
from bson import ObjectId
from flask_login import UserMixin
client = MongoClient("mongodb://localhost:27017/")
db = client['USERBASE']
collection = db['USERDATA']
user_todo = db['USERTODO']

class User(UserMixin):
    def __init__(self, user_id):
        self.user_id = ObjectId(user_id)
    def get_id(self):
        return str(self.user_id)
