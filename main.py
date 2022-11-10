import datetime
import flask
import json
import user
import shirts
import hashlib


app = flask.Flask(__name__)
app.secret_key = b'QB\xb7\x89ry\xff}\xc3\x85B\x00.\xc3\xb7\xed'

um = user.UserManager()
sm = shirts.ShirtManager()

@app.route('/')
def root():
    return flask.render_template("LoginPage.html", code=302)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)


@app.route('/Register.html', methods=['POST', 'GET'])
def register_user():
    if flask.request.method =='POST':
        fname = flask.request.form['fname']
        lname = flask.request.form['lname']
        uname = flask.request.form['username']
        email = flask.request.form['email']
        acc_type = flask.request.form['account-type']
        password = get_password_hash(flask.request.form['password'])
        if not user.is_unique("email", email):
            return flask.render_template("Register.html", error_message='Account with this email already exists')
        if not user.is_unique("username", uname):
            return flask.render_template("Register.html", error_message='Username not available')
        elif fname and lname and uname and email and password and acc_type:
            flask.session['user'] = um.register_user(fname, lname, uname, email, password, acc_type)
            return flask.redirect('/ProductPage.html')
    return flask.render_template("Register.html", code=302)
    

@app.route('/LoginPage.html', methods=['POST', 'GET'])
def login_user():
    if flask.request.method == 'POST':
        email = flask.request.form['email']
        password = hash(flask.request.form['password'])
        if email and password:
            flask.session['user'] = um.login_user(email, password)
            curr_user = get_user()
            if curr_user is not None:
                return flask.redirect('/ProductPage.html')
            else:
                return flask.render_template('/LoginPage.html', error_message='Incorrect username or password')
    return flask.render_template("LoginPage.html", code=302)

@app.route('/About.html')
def About():
    return flask.render_template("About.html", code=302)

@app.route('/ProductPage.html', methods = ['GET'])
def ProductPage():
    return flask.render_template("ProductPage.html", code=302)

@app.route('/ShirtSubmission.html', methods=['POST', 'GET'])
def shirt_submission():
    if flask.request.method == 'POST':
        designName = flask.request.form["shirtName"]
        shirtImage = flask.request.form["shirtImage"]
        curr_user = get_user()
        if curr_user:
            sm.new_design(curr_user['first_name'],designName, shirtImage)
            print("Saved New Design")
            return flask.redirect("/ShirtConfirmation.html", code=302)
    return flask.render_template("ShirtSubmission.html", code=302)

@app.route('/ShirtConfirmation.html', methods=['POST', 'GET'])
def shirt_confirmation():
    return flask.render_template("ShirtConfirmation.html", code=302)

def get_user():
    return flask.session.get('user', None)

def get_password_hash(pw):
    encoded = pw.encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()

def logout():
    flask.session['user'] = None
    return flask.redirect('LoginPage.html')