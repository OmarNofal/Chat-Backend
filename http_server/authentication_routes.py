from __main__ import app
from argparse import ArgumentError
from flask import request
from datetime import datetime

from auth.authenticator import authenticator
from http_server.api_response import error_reponse, success_response
from model.user import user
from store.profile_store import profile_store


a = authenticator.get_instance()
ps = profile_store.get_instance()

@app.route('/register', methods = ['POST'])
def register():
    data = request.json

    u : user    
    try:
        u = user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=datetime.fromisoformat(data['birth_date'] + ' 00:00:00'),
            phone_number=data['phone_number'],
            password=data['password'],
            country=data['country']
        )
    except KeyError as e:
        return error_reponse("There is a missing required field").content


    try:
        a = authenticator.get_instance()
        result = a.register(u)
        response = success_response()
        response['token'] = result['token']
        response['user_id'] = result['user_id']
        return response.content
    except ArgumentError as e:
        return error_reponse(e.message).content
    


@app.route('/login', methods = ['POST'])
def login():
    data = request.json
    
    a = authenticator.get_instance()
    try:
        token = a.login(data)
        res = success_response()
        res['token'] = token
        return res.content
    except ArgumentError as e:
        res = error_reponse(e.message)
        return res.content



