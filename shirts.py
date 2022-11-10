from google.cloud import datastore


def get_client():
    return datastore.Client()


def create_design():
    client = get_client()
    key = client.key('design')
    return datastore.Entity(key)


def update_design(design):
    client = get_client()
    client.put(design)


class ShirtManager():

    def __init__(self):
        self.user = None

    def new_design(self, designer, shirtName, shirtDesignImage):
        shirt = create_design()
        shirt['designer'] = designer
        shirt['shirtName'] = shirtName
        shirt['shirtDesignImage'] = shirtDesignImage
        update_design(shirt)
        self.shirt = shirt
        return shirt

    