from google.cloud import datastore


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
    

class UserManager():

    def __init__(self):
        self.user = None

    def register_user(self, fname, lname, email, password):
        user = create_user()
        user['first_name'] = fname
        user['last_name'] = lname
        user['email'] = email
        user['password'] = password
        update_user(user)
        self.user = user
        return user

    def login_user(self, email, password):
        client = get_client()
        query = client.query(kind='user')
        query.add_filter("email","=", email)
        query.add_filter("password","=", password)
        user = list(query.fetch())
        print(user)
        print(len(user))
        if len(user) == 1:
            self.user = user[0]
        else:
            self.user = None
        return self.user

    '''not implemented'''

    def logout(self, user):
        print()