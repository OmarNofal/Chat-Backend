from time import sleep
from flask import Flask

app = Flask(__name__)

import http_server.authentication_routes
import http_server.profile_routes
import http_server.friend_request_routes

@app.route('/')
def index():

    sleep(4)

    return 'hello'


app.run(debug=True)