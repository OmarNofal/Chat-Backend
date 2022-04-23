from datetime import datetime
from distutils.command.upload import upload
import os
import pathlib
from turtle import mode

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
            dao = app_database.get_instance().get_files_dao()
            print("Inserting model")
            d = file_model(
                id = None,
                user_id= user_id,
                file_name= file_name,
                file_extension= extension
            )
            result = dao.insert(d)

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

    def get_file_details(file_id: str):
        dao = app_database.get_instance().get_files_dao()
        file_obj = dao.find({'id': ObjectId(file_id)})
        if file_obj is None:
            return None
        
        file_details = file_obj[0]
        f = file_model(
            id=str(file_details['_id']),
            file_name=file_details['file_name'],
            file_extension=file_details['file_extension'],
            upload_date=file_details['upload_date']
        )

        return f
        

    def get_file_path(user_id: str, file_name: str):
        return _media_folder + f"{user_id}\\{file_name}"

    def delete_file(file_id: str):
        dao = app_database.get_instance().get_files_dao()
        file_details = files_store.get_file_details(file_id)
        if file_details is None:
            return
        file_name = file_details['file_name']
        user_id = file_details['user_id']
        
        dao.delete_id(file_id)

        try:
            os.remove(_media_folder + f"{user_id}\\{file_name}")
        except:
            return
