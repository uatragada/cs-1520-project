import datetime
import flask
import json
import user

app = flask.Flask(__name__)
um = user.UserManager()


@app.route('/')
def root():
    return flask.redirect("/cs/LoginPage.html", code=302)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    fname = flask.request.form['fname']
    lname = flask.request.form['lname']
    email = flask.request.form['email']
    password = flask.request.form['password']
    if fname and lname and email and password:
        um.register_user(fname, lname, email, password)


@app.route('/login', methods=['POST', 'GET'])
def login_user():
    email = flask.request.form['email']
    password = flask.request.form['password']
    if email and password:
        um.login_user(email, password)
