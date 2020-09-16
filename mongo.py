import json
from json import load
from pymongo import MongoClient
import pymongo
from pymongo import database
from pymongo.errors import DuplicateKeyError
import os

def get_client(uri="mongodb://localhost:27017/"):
    client = MongoClient(uri)
    return client


def get_database(client, database_name="scraping"):
    db = client[database_name]
    return db


def create_collection(database, collection_name="data", key="Tema"):
    collection = database[collection_name]
    collection.create_index([(key, pymongo.ASCENDING)], unique=True)
    return collection

def get_collection(database, collection_name="data"):
    collection = database[collection_name]
    return collection

def load_many_files(collection, directory="scraping_reports"):

    for file in os.listdir(directory):
        with open('{}/{}'.format(directory, file)) as f:
            file_data = json.load(f)
        try:    
            collection.insert_many(file_data, ordered=False)
        except Exception:
            pass

    cursor = collection.find({})
    print("Collection now consist of {} documents".format(collection.count_documents({})))

def load_one(collection, file):
    for object in file:
        try:
            collection.insert_one(object)
        except DuplicateKeyError:
            print("Duplicate entry")

def create_text_index(collection, keys):
    key_text = [(i, "text") for i in keys]
    collection.create_index(key_text)

def search(collection, search_text, exact=False):
    if exact:
        for i in collection.find({"$text": {"$search": "\"{}\"".format(search_text)}}).limit(10):
            print(i)
    else:
        for i in collection.find({"$text": {"$search": search_text}}).limit(100):
            print(i)
    

if __name__=="__main__":
    client = get_client()
    db = get_database(client)
    collection = get_collection(db)
    # # collection.drop()
    # collection = create_collection(db)
    # create_text_index(collection, [
    #         "Journaldato",
    #         "Avsender(e)",
    #         "Sendt",
    #         "Arkivsak",
    #         "Brevdato",
    #         "Dokumenttype",
    #         "Ansvarlig",
    #         "Saksbehandler",
    #         "Tema"
    #         ])
    load_many_files(collection)
    search(collection, "Make Sande Greit Again", exact=True)
    client.close()