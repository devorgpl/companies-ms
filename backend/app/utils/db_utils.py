import os

from pymongo import MongoClient

DB_HOST = os.environ.get("DB_HOST", 'localhost')
def companies_collection():
    client = MongoClient(DB_HOST, 27017)
    db = client['companyms']
    collection = db['companies']
    return collection


def userselection_collection():
    client = MongoClient(DB_HOST, 27017)
    db = client['companyms']
    collection = db['userselection']
    return collection
