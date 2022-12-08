import datetime
import flask
import json
import user
import shirts
import hashlib
from google.cloud import datastore

app = flask.Flask(__name__)
app.secret_key = b'QB\xb7\x89ry\xff}\xc3\x85B\x00.\xc3\xb7\xed'

um = user.UserManager()
sm = shirts.ShirtManager()

@app.route('/')
def root():
    curr_user = get_user()
    if curr_user:
        return flask.redirect('/products')
    else:
        return flask.redirect('/login')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    if flask.request.method =='POST':
        fname = flask.request.form['fname']
        lname = flask.request.form['lname']
        uname = flask.request.form['username']
        email = flask.request.form['email']
        acc_type = flask.request.form['account-type']
        password = get_password_hash(flask.request.form['password'])
        if not user.is_unique("email", email):
            return show_page("Register.html", err='Account with this email already exists')
        if not user.is_unique("username", uname):
            return show_page("Register.html", err='Username not available')
        elif fname and lname and uname and email and password and acc_type:
            flask.session['user'] = um.register_user(fname, lname, uname, email, password, acc_type)
            return flask.redirect('/products')
    return show_page("/Register.html")
    

@app.route('/login', methods=['POST', 'GET'])
def login_user():
    if flask.request.method == 'POST':
        email = flask.request.form['email']
        password = get_password_hash(flask.request.form['password'])
        if email and password:
            flask.session['user'] = um.login_user(email, password)
            curr_user = get_user()
            if curr_user is not None:
                return flask.redirect('/products')
            else:
                return show_page('/LoginPage.html', err='Incorrect email or password')
    return show_page("/LoginPage.html")

@app.route('/about')
def About():
    return show_page("/About.html")

@app.route('/products', methods = ['GET'])
def ProductPage():
    return show_page("/ProductPage.html")

@app.route('/account', methods=['POST', 'GET'])
def Account():
    
    '''
    if flask.request.method == 'POST':
        curr_user = get_user()
        curr_user['acc_type'] = flask.request.form['account-type']
       # print(flask.request.form['account-type'])
       # um.update(curr_user)
        return flask.redirect('/account')
        '''
    return show_page("/AccountInfo.html", designs=get_designs())

@app.route('/shirt-submission', methods=['POST', 'GET'])
def shirt_submission():
    if flask.request.method == 'POST':
        designName = flask.request.form["shirtName"]
        shirtImage = flask.request.form["shirtImage"]
        curr_user = get_user()
        if curr_user:
            sm.new_design(curr_user['first_name'],designName, shirtImage)
            print("Saved New Design")
            return flask.redirect('/shirt-confirmation')
    return show_page("ShirtSubmission.html")


@app.route('/shirt-confirmation', methods=['POST', 'GET'])
def shirt_confirmation():
    return show_page("ShirtConfirmation.html")


def get_user():
    return flask.session.get('user', None)

def get_password_hash(pw):
    encoded = pw.encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()

@app.route('/logout')
def logout():
    flask.session['user'] = None
    return flask.redirect('/login')

def show_page(page, err=None, designs=None):
    return flask.render_template(page, current_user=get_user(), error_message=err, designs=designs)

def get_client():
    return datastore.Client()

def get_designs():
    client = get_client()
    query = client.query(kind='design')
    curr_user = get_user()
    query.add_filter('designer', '=', curr_user.get('first_name'))
    designs = list(query.fetch())
    return designs