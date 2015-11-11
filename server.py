from flask import Flask, flash, session, request, render_template, redirect
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import re
NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
app = Flask(__name__)
app.secret_key = 'InvestED'
mysql = MySQLConnector('loginregdb')
bcrypt = Bcrypt(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/register', methods=['POST'])
def reg():
  counter = 0
  flash('') #I think returning a success flash could eliminate this problem.
  session['first_name']   = request.form['first_name']
  session['last_name']    = request.form['last_name']
  session['email']        = request.form['email']
  password                = request.form['password']
  confirm                 = request.form['confirm']

  if not NAME_REGEX.match(session['first_name']):
    flash('Your first name can only contain letters & must be at least \
          2 characters.')
    counter += 1
  if not NAME_REGEX.match(session['last_name']):
    flash('Your last name can only contain letters & must be at least \
          2 characters.')
    counter += 1
  if not EMAIL_REGEX.match(session['email']):
    flash('Not a valid email.')
    counter += 1
  if password != confirm:
    flash("Confirmation does not match Password, please re-enter.")
    counter += 1
  elif len(request.form['password']) < 8:
    flash("Password must be at least 8 characters long")
    counter += 1
  if counter != 0:
    return redirect('/')
  else:
    check = mysql.fetch("SELECT email FROM users \
                        WHERE email = '{}'".format(session['email']))
    if len(check) > 0:
      flash('That email is already in the database.  Please login.')
      return render_template('index.html')
    else:

      insert = "INSERT INTO users \
                (first_name, last_name, email, pw_digest, created_at, updated_at) \
                VALUES ('{}','{}','{}','{}', NOW(), NOW())".format(session['first_name'], session['last_name'], session['email'], pw_hash)
      mysql.run_mysql_query(insert)
      flash('Welcome to the machine.')
      return redirect('/users')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/login', methods=['POST'])
def logcheck():
    user = mysql.fetch("SELECT * FROM users \
                        WHERE email = '{}' LIMIT 1".format(request.form['email']))
    if len(user) < 0:
      flash('Email not in database. Please register.')
      return render_template('index.html')
    else:
      if bcrypt.check_password_hash(user[0]['pw_digest'], request.form['password']):
        flash('Welcome back!')
        return redirect('/users')
      else:
        flash('Email and/or Password not correct')
        return redirect('/login')

@app.route('/users')
def users():
  users = mysql.fetch("SELECT first_name, last_name, email, created_at \
                       FROM users")
  return render_template('users.html', users = users)

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')

app.run(debug=True)

