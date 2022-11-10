import datetime
import flask
import json
import user

import shirts

app = flask.Flask(__name__)
# um = user.UserManager()

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
        email = flask.request.form['email']
        password = flask.request.form['password']
        if fname and lname and email and password:
             um.register_user(fname, lname, email, password)
             print("REGISTERING")
             return flask.redirect('/ProductPage.html')
    return flask.render_template("Register.html", code=302)
    


@app.route('/LoginPage.html', methods=['POST', 'GET'])
def login_user():
    if flask.request.method == 'POST':
        email = flask.request.form['email']
        password = flask.request.form['password']
        if email and password:
            um.login_user(email, password)
            if um.user is not None:
                print("Logging User In")
                return flask.redirect('/ProductPage.html')
            
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
        sm.new_design(um.user["first_name"],designName, shirtImage)
        print("Saved New Design")
        return flask.redirect("/ShirtConfimation.html", code=302)
    return flask.render_template("ShirtSubmission.html", code=302)

@app.route('/ShirtConfirmation.html', methods=['POST', 'GET'])
def shirt_confirmation():
    return flask.render_template("ShirtConfirmation.html", code=302)