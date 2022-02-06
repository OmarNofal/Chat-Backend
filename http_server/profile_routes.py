from __main__ import app
from flask import request
from datetime import datetime

from auth.authenticator import authenticator
from model.user import user
from store.profile_store import profile_store


a = authenticator.get_instance()
ps = profile_store.get_instance()



@app.route('/viewProfile', methods = ['GET'])
def view_profile():
    data = request.json
    
    try:
        token = data['token']
        user_id = data['user_id']
        
        if not a.get_user_id(token):
            return {'result': 'error', 'message': 'Missing or invalid token'}

        return ps.get_user_profile(user_id)
    except Exception as e:
        return {'result': 'error', 'message': str(e)}

