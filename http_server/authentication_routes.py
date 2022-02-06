from __main__ import app
from flask import request
from datetime import datetime

from auth.authenticator import authenticator
from model.user import user
from store.profile_store import profile_store


a = authenticator.get_instance()
ps = profile_store.get_instance()

@app.route('/register', methods = ['POST'])
def register():
    data = request.json
    
    u = user(
        first_name=data['first_name'],
        last_name=data['last_name'],
        birth_date=datetime.fromisoformat(data['birth_date'] + ' 00:00:00'),
        phone_number=data['phone_number'],
        password=data['password'],
        country=data['country']
    )

    a = authenticator.get_instance()
    result = a.register(u)
    return result


@app.route('/login', methods = ['POST'])
def login():
    data = request.json
    
    a = authenticator.get_instance()
    result = a.login(data)
    return result



