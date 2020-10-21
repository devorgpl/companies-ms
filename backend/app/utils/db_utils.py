from pymongo import MongoClient


def companies_collection():
    client = MongoClient('localhost', 27017)
    db = client['companyms']
    collection = db['companies']
    return collection


def userselection_collection():
    client = MongoClient('localhost', 27017)
    db = client['companyms']
    collection = db['userselection']
    return collection
