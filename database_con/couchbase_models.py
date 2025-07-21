# couchbase_models.py
from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator

cluster = Cluster('couchbase://localhost', ClusterOptions(
    PasswordAuthenticator('username', 'password')))
bucket = cluster.bucket('your_bucket')
collection = bucket.default_collection()

class CouchbaseUser:
    def __init__(self, user_id=None, data=None):
        self.user_id = user_id
        self.data = data or {}

    def save(self):
        if not self.user_id:
            raise Exception("user_id required")
        collection.upsert(self.user_id, self.data)

    def delete(self):
        if self.user_id:
            collection.remove(self.user_id)

    @classmethod
    def get(cls, user_id):
        try:
            result = collection.get(user_id)
            return cls(user_id, result.content_as[dict])
        except Exception:
            return None

    @classmethod
    def all(cls):
        # Couchbase does not support .all() like SQL. Use a N1QL query:
        query = f'SELECT META().id, * FROM `your_bucket` WHERE type="user"'
        rows = cluster.query(query)
        return [cls(row['id'], row['your_bucket']) for row in rows]
