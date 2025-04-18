import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase Service Account Key
cred = credentials.Certificate("D:\Business Plan\App features\deliqobot-firebase-adminsdk-fbsvc-82cee265c7.json")
firebase_admin.initialize_app(cred)

# Firestore Database Instance
db = firestore.client()
