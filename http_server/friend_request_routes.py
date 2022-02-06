from __main__ import app
from flask import request, Response, jsonify, redirect
from datetime import datetime

from auth.authenticator import authenticator
from model.user import user
from store.profile_store import profile_store
from store.requests_store import requests_store

from db.database import app_database
from bson import ObjectId

import json

def _remove_obj_id(doc):
    doc['id'] = str(doc['_id'])
    del doc['_id']

    return doc

a = authenticator.get_instance()
ps = profile_store.get_instance()
rs = requests_store.get_instance()

@app.route('/send_friend_request')
def send_friend_request():
    data = request.json

    token = data['token']
    receiver_id = data['receiver_id']

    sender_id = a.get_user_id(token)
    if not sender_id:
        return {'result': 'error', 'message': 'Missing or Invalid token'}
    
    return rs.send_request(sender_id, receiver_id)

@app.route('/get_my_requests')
def get_my_requests():
    token = request.json['token']

    user_id = a.get_user_id(token)
    if not user_id:
        return {'result': 'error', 'message': 'Missing or Invalid token'}

    res = list(map(lambda x : _remove_obj_id(x), rs.get_user_requests(user_id)))

    return jsonify(res)

@app.route('/accept_request')
def accept_request():
    token = request.json['token']
    friend_request_id = request.json['friend_request_id']


    user_id = a.get_user_id(token)
    if not user_id:
        return {'result': 'error', 'message': 'Missing or Invalid token'}

    req_dao = app_database.get_instance().get_requests_dao()
    req = req_dao.find_one({'_id': ObjectId(friend_request_id), 'receiver_id': user_id})

    if not req:
        return {'result': 'error', 'message': 'Invalid friend request id'}
    
    return rs.accept_request(friend_request_id)


@app.route('/reject_request')
def reject_request():
    token = request.json['token']
    friend_request_id = request.json['friend_request_id']


    user_id = a.get_user_id(token)
    if not user_id:
        return {'result': 'error', 'message': 'Missing or Invalid token'}

    return rs.cancel_request(friend_request_id)

@app.route('/cancel_request')
def cancel_request():
    return redirect('/reject_request')