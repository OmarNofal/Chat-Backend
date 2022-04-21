from datetime import datetime
import os
import pathlib
from turtle import mode
from isort import file
from db.files import files_dao
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
from db.database import app_database
from model.file import file as file_model

# where all media are stored
_media_folder = "C:\\Users\\omarw\\Documents\\Media Upload\\"

class files_store:


    def upload_file(user_id: str, file_name: str, 
    file_bytes: bytes, extension: str):   

        try:     
        #insert to database to get id
            dao = files_dao(app_database.get_instance().db)
            print("Inserting model")
            d = file_model(
                id = None,
                user_id= user_id,
                file_name= file_name,
                file_extension= extension
            )
            result = dao.insert(d)
            print("Model Inserted: ", str(result))
           
            #save file
            user_path = _media_folder + f"{user_id}\\"

            pathlib.Path(user_path).mkdir(parents=True, exist_ok=True, mode=777)

            file = open(user_path + f"{file_name}", 'wb')
            file.write(file_bytes)
            file.close()

            return {'result': 'success', 'media_id': str(result.inserted_id)}
        except Exception as e:
            print(e)
            return {'result': 'error', 'message': 'Failed to upload the file'}

    def get_file_detials(file_id: str):
        dao = files_dao(app_database.get_instance().db)
        file_obj = dao.find({'id': ObjectId(file_id)})
        if file_obj is None:
            return None
        
        return file_obj[0]
        

    def delete_file(file_id: str):
        dao = files_dao(app_database.get_instance().db)
        file_details = files_store.get_file_detials(file_id)
        if file_details is None:
            return
        file_id = file_details['id']
        user_id = file_details['user_id']
        
        dao.delete_id(file_id)

        try:
            os.remove(_media_folder + f"{user_id}\\{file_id}")
        except:
            return
