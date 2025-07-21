# firebase_models.py
from firebase_admin import firestore

db = firestore.client()

class FirebaseUser:
    def __init__(self, user_id=None, data=None):
        self.collection = db.collection('users')
        self.user_id = user_id
        self.data = data or {}

    def save(self):
        if self.user_id:
            self.collection.document(self.user_id).set(self.data)
        else:
            doc_ref = self.collection.document()
            doc_ref.set(self.data)
            self.user_id = doc_ref.id

    def delete(self):
        if self.user_id:
            self.collection.document(self.user_id).delete()

    @classmethod
    def get(cls, user_id):
        doc = db.collection('users').document(user_id).get()
        if doc.exists:
            return cls(user_id, doc.to_dict())
        return None

    @classmethod
    def all(cls):
        docs = db.collection('users').stream()
        return [cls(doc.id, doc.to_dict()) for doc in docs]
