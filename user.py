from google.cloud import datastore
import flask

def get_client():
    return datastore.Client()


def create_user():
    client = get_client()
    key = client.key('user')
    return datastore.Entity(key)


def update_user(user):
    client = get_client()
    client.put(user)
    print(user)
    
def is_unique(field_name, user_input):
    client = get_client()
    query = client.query(kind='user')
    query.add_filter(field_name,"=", user_input)
    user = list(query.fetch())
    if len(user) > 0:
        return False
    return True

class UserManager():

    def __init__(self):
        self.user = None

    def register_user(self, fname, lname, uname, email, password, acc_type):
        user = create_user()
        user['first_name'] = fname
        user['last_name'] = lname
        user['username'] = uname
        user['email'] = email
        user['password'] = password
        user['acc_type'] = acc_type
        update_user(user)
        self.user = user
        return self.user

    def login_user(self, email, password):
        client = get_client()
        query = client.query(kind='user')
        query.add_filter("email","=", email)
        query.add_filter("password","=", password)
        user = list(query.fetch())
        #print(user)
        #print(len(user))
        if len(user) == 1:
            self.user = user[0]
        else:
            self.user = None
        return self.user
        
    def update(self, user):
        update_user(user)

