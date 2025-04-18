import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"D:\Business Plan\App features\deliqobot-firebase-adminsdk-fbsvc-82cee265c7.json")  # Update path
firebase_admin.initialize_app(cred)

db = firestore.client()

# Test Firestore Write
doc_ref = db.collection("test").document("sample")
doc_ref.set({"message": "Hello, Firebase!"})

print("✅ Firestore is working!")
