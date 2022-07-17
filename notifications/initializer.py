import firebase_admin
from firebase_admin import credentials

cred =  credentials.Certificate("notifications/chat-38793-firebase-adminsdk-1anb7-4c171c49bf.json")
app = firebase_admin.initialize_app(cred)
