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

