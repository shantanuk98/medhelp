from flask import Flask, render_template, flash, request, url_for, redirect, session, escape
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
import gc
import mysql.connector
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="mydatabase"
)


UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

mycursor = mydb.cursor()

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = os.path.join(UPLOAD_FOLDER,"static/profile")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/profile')
def profile():
    return render_template("profile.html")

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
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index2.html', session_user_name=username_session)
    return render_template('index.html')

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
            file = request.files['file']
            if file and allowed_file(file.filename):
                x=file.filename.rsplit('.', 1)[1].lower()
                filename = str(username)+x
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            s = "insert into users(user_name, user_email, user_address, password) values(%s,%s,%s,%s)"
            v=(username,email,address,password)
            #"INSERT INTO users (user_name, user_email, user_address,  password) VALUES ( %s, %s, %s, %s);",(username, email, address, password)
            mycursor.execute(s,v)
            mydb.commit()
            return redirect(url_for('profile'))
        return render_template("signup.html", form=form)

    except Exception as e:
        return(str(e))


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    error = None
    if 'username' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        mycursor.execute("SELECT COUNT(1) FROM users WHERE user_name = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if mycursor.fetchone()[0]:
            mycursor.execute("SELECT password FROM users WHERE user_name = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            for row in mycursor.fetchall():
                if password_form == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('profile'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('homepage'))

if __name__ == "__main__":
    app.run(debug=True)
