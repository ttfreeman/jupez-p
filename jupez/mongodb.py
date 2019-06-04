from flask_pymongo import PyMongo
from bson.objectid import ObjectId

builtin_list = list

mongo = None


def _id(id):
    if not isinstance(id, ObjectId):
        return ObjectId(id)
    return id


# [START from_mongo]
def from_mongo(data):
    """
    Translates the MongoDB dictionary format into the format that's expected
    by the application.
    """
    if not data:
        return None

    data['id'] = str(data['_id'])
    return data
# [END from_mongo]


def init_app(app):
    global mongo

    mongo = PyMongo(app)
    mongo.init_app(app)


def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0

    results = mongo.db.jupes.find(skip=cursor, limit=10).sort('title')
    jupes = builtin_list(map(from_mongo, results))

    next_page = cursor + limit if len(jupes) == limit else None
    return (jupes, next_page)


def read(id):
    result = mongo.db.jupes.find_one({'_id': _id(id)})
    return from_mongo(result)


def create(data):
    result = mongo.db.jupes.insert_one(data)
    return read(result.inserted_id)


def update(data, id):
    mongo.db.jupes.replace_one({'_id': _id(id)}, data)
    return read(id)


def delete(id):
    mongo.db.jupes.delete_one({'_id': _id(id)})