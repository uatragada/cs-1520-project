class User():
    
    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
    
    def __repr__(self):
        return '<User %r>' % self.username