from google.cloud import datastore

class shirtManager():

    def __init__(self):
        self.user = None

    def new_design(self, name, username, shirtImage):
        shirt = create_design()
        shirt['creator'] = username
        shirt['designName'] = name
        shirt['shirtImage'] = shirtImage
        update_user(shirt)
        self.shirt = shirt
        return shirt

