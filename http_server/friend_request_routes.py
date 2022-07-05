from __main__ import app
from flask import request, Response, jsonify, redirect
from datetime import datetime

from auth.authenticator import authenticator
from http_server.api_response import error_reponse, success_response
from model.user import user
from store.profile_store import profile_store
from store.requests_store import requests_store

from db.database import app_database
from bson import ObjectId



def _remove_obj_id(doc):
    doc['id'] = str(doc['_id'])
    del doc['_id']

    return doc

a = authenticator.get_instance()
ps = profile_store.get_instance()
rs = requests_store.get_instance()

@app.route('/send_request', methods=['POST'])
def send_friend_request():
    data = request.json

    token = data['token']
    receiver_id = data['receiver_id']

    sender_id = a.get_user_id(token)
    if not sender_id:
        return error_reponse("Invalid Token").content
    
    id = rs.send_request(sender_id, receiver_id)
    if not id:
        return error_reponse("Could not send the friend request").content

    res = success_response()
    res['friend_request_id'] = id
    return res.content

@app.route('/get_my_requests', methods=['POST'])
def get_my_requests():
    token = request.json['token']

    user_id = a.get_user_id(token)
    if not user_id:
        return error_reponse("Invalid Token").content

    requests = list(map(lambda x : _remove_obj_id(x), rs.get_user_requests(user_id)))

    msg = success_response()
    msg['requests'] = requests

    return msg.content

@app.route('/accept_request', methods=['POST'])
def accept_request():
    token = request.json['token']
    friend_request_id = request.json['friend_request_id']


    user_id = a.get_user_id(token)
    if not user_id:
        return error_reponse("Invalid Token").content

    req_dao = app_database.get_instance().get_requests_dao()
    req = req_dao.find_one({'_id': ObjectId(friend_request_id), 'receiver_id': user_id})

    if not req:
        return error_reponse("Invalid Friend Request Id").content
    
    res = rs.accept_request(friend_request_id)

    if not res:
        return error_reponse("Error occured while accepting friend request").content

    return success_response().content


@app.route('/reject_request', methods=['POST', 'GET'])
def reject_request():
    token = request.json['token']
    friend_request_id = request.json['friend_request_id']


    user_id = a.get_user_id(token)
    if not user_id:
        return error_reponse("Invalid Token").content

    result = rs.cancel_request(friend_request_id)
    if not result:
        return error_reponse("Error occured while canceling a friend request").content

    return success_response().content

@app.route('/cancel_request', methods=['POST'])
def cancel_request():
    return redirect('/reject_request', code = 307)


@app.route('/get_my_friends', methods = ["POST"])
def get_my_friends():
    data = request.json

    token = data["token"]
    user_id = authenticator.get_instance().get_user_id(token)
    if not user_id:
        return error_reponse("Invalid token").content

    friends = rs.get_friends_of(user_id)
    response = success_response()
    response["friends"] = list(map(lambda x: _remove_obj_id(x), friends))

    return response.content