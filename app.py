from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
import gc
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="shan",
  passwd="password",
  database="mydatabase"
)

print(mydb)

mycursor = mydb.cursor()

app = Flask(__name__)

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = TextField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = TextField('Repeat Password')
    address = TextField('Address', [validators.Length(min=0, max=200)])
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])


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

@app.route('/signup', methods=["GET","POST"])
def signup_page():
    try:
        form = RegistrationForm(request.form)
        print("hi")
        if request.method == "POST":
            print('hello from if')
            username  = str(form.username.data)
            email = str(form.email.data)
            password = str(form.password.data)
            address = str(form.address.data)
            s = "insert into users(user_name, user_email, user_address, password) values(%s,%s,%s,%s)"
            v=(username,email,address,password)
            print(s)
            #"INSERT INTO users (user_name, user_email, user_address,  password) VALUES ( %s, %s, %s, %s);",(username, email, address, password)
            mycursor.execute(s,v)
            mydb.commit()
        return render_template("signup.html", form=form)

    except Exception as e:
        return(str(e))


# Route for handling the login page logic
@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('homepage'))
    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run(debug=True)
