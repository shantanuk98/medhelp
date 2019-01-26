from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
import gc
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="lab3@cc",
  database="mydatabase"
)

print(mydb)

mycursor = mydb.cursor()

app = Flask(__name__)

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])

@app.route('/signup')
def signup_page():
	return render_template("signup.html")

@app.route('/login')
def login_page():
	return render_template("login.html")

@app.route('/medicine')
def medicine_page():
	return render_template("medicine.html")

@app.route('/donate')
def donate_page():
	return render_template("donate.html")

@app.route('/volunteer')
def volunteer_page():
	return render_template("volunteer.html")

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/register', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))


@app.route('/login', methods=["GET","POST"])
def login_page():

    error = ''
    try:

        if request.method == "POST":

            attempted_username = request.form['username']
            attempted_password = request.form['password']

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('main.html'))

            else:
                error = "Invalid credentials. Try Again."

        return render_template("login.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("login.html", error = error)


if __name__ == "__main__":
    app.run()
