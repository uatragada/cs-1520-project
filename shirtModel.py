class User():
    
    def __init__(self, name, username, shirtImage):
        self.creator = username
        self.designName = name
        self.shirtImage = shirtImage
    
    def __repr__(self):
        return '<Shirt Design %r>' % self.designName