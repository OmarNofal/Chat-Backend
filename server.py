from time import sleep
from flask import Flask

app = Flask(__name__)

import http_server.authentication_routes
import http_server.profile_routes
import http_server.friend_request_routes
import http_server.friend_routes

@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':
   app.run(host='0.0.0.0')
   app.run(debug=True)