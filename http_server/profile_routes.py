from __main__ import app
from time import sleep
from flask import request
from datetime import datetime

from auth.authenticator import authenticator
from http_server.api_response import error_reponse, success_response
from model.user import user
from store.profile_store import profile_store


a = authenticator.get_instance()
ps = profile_store.get_instance()


@app.route('/updateProfile', methods = ['POST'])
def update_profile():
    data = request.json

    token = data['token']
    
    user_id = a.get_user_id(token)
    if not user_id:
        return error_reponse("Invalid Token").content
    

    u = ps.get_user_profile(user_id = user_id)

    if not u:
        return error_reponse("Invalid User Id").content

    for key, value in data['user'].items():
        if key == "id" or key == "password":
            return error_reponse("Can't change id or password of the User").content
        setattr(u, key, value)
    ps.update_user_profile(u)

    return success_response().content




@app.route('/viewProfile', methods = ['GET', 'POST'])
def view_profile():
    data = request.json
   
    token = data['token']
    user_id = data['user_id']
        
    if not a.get_user_id(token):
        return error_reponse("Invalid Token").content

    user = ps.get_user_profile(user_id)
    if user == None:
        return error_reponse("User not found").content

    res = success_response()
    res['user'] = user.as_dict()
    return res.content


@app.route('/searchUsers', methods = ['GET', 'POST'])
def search_users():
    data = request.json

    token = data['token']
    query = data['query']

    if not a.get_user_id(token):
        return error_reponse("Invalid Token").content

    res = success_response()
    users: list[user] = ps.search_users(query = query)
    res['users'] = list(map(lambda x: x.as_dict(), users))
    return res.content
