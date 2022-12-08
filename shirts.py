from google.cloud import datastore
from datetime import datetime

def get_client():
    return datastore.Client()


def create_design():
    client = get_client()
    key = client.key('design')
    return datastore.Entity(key)


def update_design(design):
    client = get_client()
    client.put(design)

def get_designs():
    client = get_client()
    query = client.query(kind='design')
    shirtsList = list(query.fetch())
    for shirt in shirtsList:
        print(shirt)
        print('\n')
    return shirtsList

class ShirtManager():

    def __init__(self):
        self.shirt = None

    def new_design(self, designer, shirtName, shirtDesignImage):
        shirt = create_design()
        shirt['designer'] = designer
        shirt['shirtName'] = shirtName
        shirt['shirtDesignImage'] = shirtDesignImage
        shirt['dateCreated'] = datetime.now()
        update_design(shirt)
        self.shirt = shirt
        print(shirt)
        get_designs()
        return self.shirt

    