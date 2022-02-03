import pymongo
from bson.objectid import ObjectId
from model import model

class dao:

    def __init__(self, db: pymongo.database.Database, collection_name):
        print(db)
        self.collection = db.get_collection(collection_name)

    def insert(self, x: model.model):
        obj = x.as_dict()
        del obj['id']

        return self.collection.insert_one(obj)

    def delete(self, x: model.model):
        obj = x.as_dict()
        del obj['id']
        
        return self.collection.delete_one(obj)
    
    def delete_id(self, id: str):
        object_id = ObjectId(id)

        return self.collection.delete_one({'_id': object_id})
    
    def update(self, x: model.model):
        obj = x.as_dict()
        obj['_id'] = ObjectId(obj['id'])
        del obj['id']

        return self.collection.update_one(obj)

    def find_one(self, x: dict):
        
        if 'id' in x:
            x['_id'] = ObjectId(x['id'])
            del x['id']
        
        return self.collection.find_one(x)
    

    def find(self, x: dict):
        
        if 'id' in x:
            x['_id'] = ObjectId(x['id'])
            del x['id']
        
        return self.collection.find(filter=x)